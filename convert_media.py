#!/usr/bin/env python3
"""Convert HEIC images to JPG and MOV videos to MKV (H.265, Full HD)."""

from __future__ import annotations
import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from typing import Iterable

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. Install with: pip install Pillow pillow-heif"
    ) from exc

try:
    from pillow_heif import register_heif_opener
except ImportError as exc:
    raise SystemExit(
        "pillow-heif is required for HEIC support. Install with: pip install pillow-heif"
    ) from exc

register_heif_opener()

IMAGE_EXTENSIONS = {'.heic'}
VIDEO_EXTENSIONS = {'.mov'}


def is_ffmpeg_available(ffmpeg_path: str) -> bool:
    if shutil.which(ffmpeg_path):
        return True
    # Check common FFmpeg installation paths on Windows
    if platform.system() == 'Windows':
        import os
        local_appdata = os.environ.get('LOCALAPPDATA')
        if local_appdata:
            winget_path = Path(local_appdata) / 'Microsoft' / 'WinGet' / 'Packages'
            if winget_path.exists():
                for pkg_dir in winget_path.glob('Gyan.FFmpeg*'):
                    ffmpeg_exe = pkg_dir / 'bin' / 'ffmpeg.exe'
                    if ffmpeg_exe.exists():
                        return True
        # Check Program Files
        program_files = [os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)')]
        for pf in program_files:
            if pf:
                ffmpeg_exe = Path(pf) / 'ffmpeg' / 'bin' / 'ffmpeg.exe'
                if ffmpeg_exe.exists():
                    return True
    return False


def find_ffmpeg_path() -> str | None:
    if shutil.which('ffmpeg'):
        return 'ffmpeg'
    # Check common FFmpeg installation paths on Windows
    if platform.system() == 'Windows':
        import os
        local_appdata = os.environ.get('LOCALAPPDATA')
        program_files = os.environ.get('ProgramFiles')
        program_files_x86 = os.environ.get('ProgramFiles(x86)')
        
        # Winget path
        if local_appdata:
            winget_path = Path(local_appdata) / 'Microsoft' / 'WinGet' / 'Packages'
            if winget_path.exists():
                for pkg_dir in winget_path.glob('Gyan.FFmpeg*'):
                    for bin_dir in pkg_dir.rglob('bin'):
                        ffmpeg_exe = bin_dir / 'ffmpeg.exe'
                        if ffmpeg_exe.exists():
                            return str(ffmpeg_exe)
        
        # Common installation paths
        common_paths = [
            Path('C:') / 'ffmpeg' / 'bin' / 'ffmpeg.exe',
        ]
        if program_files:
            common_paths.append(Path(program_files) / 'ffmpeg' / 'bin' / 'ffmpeg.exe')
        if program_files_x86:
            common_paths.append(Path(program_files_x86) / 'ffmpeg' / 'bin' / 'ffmpeg.exe')
        if local_appdata:
            common_paths.append(Path(local_appdata) / 'Programs' / 'ffmpeg' / 'bin' / 'ffmpeg.exe')
        
        for p in common_paths:
            if p.exists():
                return str(p)
    return None


def install_ffmpeg_interactively() -> None:
    if not sys.stdin.isatty():
        raise SystemExit(
            'FFmpeg not found and no interactive terminal is available to install it.'
        )

    answer = input(
        'FFmpeg is required to convert MOV files to MKV. Install now? [y/N]: '
    ).strip().lower()
    if answer not in {'y', 'yes'}:
        raise SystemExit('FFmpeg is required. Install it manually and rerun.')

    system = platform.system()
    if system == 'Windows':
        winget = shutil.which('winget')
        choco = shutil.which('choco')
        if winget:
            try:
                result = subprocess.run(
                    [
                        winget,
                        'install',
                        '-e',
                        '--id',
                        'Gyan.FFmpeg',
                        '--accept-package-agreements',
                        '--accept-source-agreements',
                    ],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 or 'already installed' in result.stdout.lower():
                    print('FFmpeg installation completed or already installed.')
                else:
                    print(f'Winget output: {result.stdout}')
                    print(f'Winget error: {result.stderr}')
                    raise SystemExit('Winget installation failed.')
            except FileNotFoundError:
                raise SystemExit('Winget not found.')
        elif choco:
            subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)
        else:
            raise SystemExit(
                'No supported installer found (winget or choco). '
                'Install FFmpeg manually from https://ffmpeg.org.'
            )
    elif system == 'Darwin':
        brew = shutil.which('brew')
        if brew:
            subprocess.run([brew, 'install', 'ffmpeg'], check=True)
        else:
            raise SystemExit('Homebrew not found. Install FFmpeg manually first.')
    else:
        apt = shutil.which('apt-get')
        yum = shutil.which('yum')
        pacman = shutil.which('pacman')
        if apt:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
        elif yum:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'ffmpeg'], check=True)
        elif pacman:
            subprocess.run(['sudo', 'pacman', '-Sy', 'ffmpeg'], check=True)
        else:
            raise SystemExit(
                'No known package manager found. Install FFmpeg manually from https://ffmpeg.org.'
            )

    print('FFmpeg installation attempt completed.')


def ensure_ffmpeg_installed(ffmpeg_path: str) -> str:
    if is_ffmpeg_available(ffmpeg_path):
        return ffmpeg_path
    found_path = find_ffmpeg_path()
    if found_path:
        return found_path
    install_ffmpeg_interactively()
    found_path = find_ffmpeg_path()
    if found_path:
        return found_path
    if not is_ffmpeg_available(ffmpeg_path):
        raise SystemExit('FFmpeg was not found after the installation attempt.')
    return ffmpeg_path


def convert_heic_to_jpg(source_path: Path, quality: int = 95) -> Path:
    output_path = source_path.with_suffix('.jpg')
    if output_path.exists():
        print(f"Skipping existing JPG: {output_path.name}")
        return output_path

    try:
        Image.register_extension(Image.Image, '.heic')
    except Exception:
        pass

    with Image.open(source_path) as image:
        rgb = image.convert('RGB')
        rgb.save(output_path, format='JPEG', quality=quality, optimize=True)

    print(f"Converted: {source_path.name} -> {output_path.name}")
    return output_path


def convert_mov_to_mkv(source_path: Path, ffmpeg_path: str = 'ffmpeg') -> Path:
    output_path = source_path.with_suffix('.mkv')

    if output_path.exists():
        print(f"Skipping existing MKV: {output_path.name}")
        return output_path

    ffmpeg_args = [
        ffmpeg_path,
        '-y',
        '-hide_banner',
        '-loglevel', 'error',
        '-i', str(source_path),

        # Preserve original video resolution/orientation
        '-map_metadata', '0',
        '-movflags', 'use_metadata_tags',

        # Video encoding
        '-c:v', 'libx265',
        '-preset', 'medium',
        '-crf', '23',

        # Preserve audio
        '-c:a', 'aac',
        '-b:a', '192k',

        str(output_path),
    ]

    subprocess.run(ffmpeg_args, check=True)

    print(f"Converted: {source_path.name} -> {output_path.name}")

    return output_path


def find_files(folder: Path, extensions: Iterable[str]) -> list[Path]:
    return [item for item in folder.iterdir() if item.is_file() and item.suffix.lower() in extensions]


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Convert HEIC images to JPG and MOV videos to MKV with H.265 / Full HD.'
    )
    parser.add_argument('root', nargs='?', default='.', help='Root folder containing Images and Videos folders')
    parser.add_argument('--jpg-quality', type=int, default=95, help='JPEG quality for converted images (default: 95)')
    parser.add_argument('--ffmpeg', default='ffmpeg', help='FFmpeg executable path (default: ffmpeg)')
    args = parser.parse_args()

    root_folder = Path(args.root).expanduser().resolve()
    images_folder = root_folder / 'Images'
    videos_folder = root_folder / 'Videos'

    if not images_folder.is_dir():
        raise SystemExit(f"Images folder not found: {images_folder}")
    if not videos_folder.is_dir():
        raise SystemExit(f"Videos folder not found: {videos_folder}")

    heic_files = find_files(images_folder, IMAGE_EXTENSIONS)
    mov_files = find_files(videos_folder, VIDEO_EXTENSIONS)

    if not heic_files and not mov_files:
        print('No HEIC images or MOV videos found to convert.')
        return

    for heic in heic_files:
        convert_heic_to_jpg(heic, quality=args.jpg_quality)

    if mov_files:
        ffmpeg_path = ensure_ffmpeg_installed(args.ffmpeg)
        for mov in mov_files:
            convert_mov_to_mkv(mov, ffmpeg_path=ffmpeg_path)

    print('Conversion complete.')


if __name__ == '__main__':
    main()
