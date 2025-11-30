"""Django management command to download vendor static files."""

from pathlib import Path
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from helpers import download_to_local


# Vendor static files to download
VENDOR_STATICFILES = {
    "saas-theme.min.css": "https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css",
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map",
}


class Command(BaseCommand):
    """Download and update vendor static files from external sources."""

    help = (
        "Download vendor static files (CSS, JS) from CDNs and external sources"
    )

    def add_arguments(self, parser):
        """Add custom command arguments."""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force download even if files already exist",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command to download vendor files.

        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments including 'force' flag

        Raises:
            CommandError: If STATICFILES_VENDOR_DIR is not configured
        """
        # Validate settings
        vendors_dir = self._get_vendors_directory()
        force_download = options.get("force", False)

        # Start download process
        self.stdout.write(
            self.style.MIGRATE_HEADING("Downloading vendor static files...")
        )
        self.stdout.write(f"Target directory: {vendors_dir}\n")

        # Download files
        completed_urls = []
        failed_downloads = []

        for filename, url in VENDOR_STATICFILES.items():
            out_path = vendors_dir / filename

            # Check if file exists
            if out_path.exists() and not force_download:
                self.stdout.write(
                    self.style.WARNING(
                        f"⏭️  Skipping {filename} (already exists)"
                    )
                )
                completed_urls.append(url)
                continue

            # Download file
            self.stdout.write(f"⬇️  Downloading {filename}...", ending=" ")
            dl_success = download_to_local(url, out_path)

            if dl_success:
                completed_urls.append(url)
                self.stdout.write(self.style.SUCCESS("✓"))
            else:
                failed_downloads.append((filename, url))
                self.stdout.write(self.style.ERROR("✗"))

        # Display results
        self._display_results(completed_urls, failed_downloads)

    def _get_vendors_directory(self) -> Path:
        """Get and validate the vendors directory from settings.

        Returns:
            Path: The vendors directory path

        Raises:
            CommandError: If STATICFILES_VENDOR_DIR is not configured
        """
        try:
            vendors_dir = getattr(settings, "STATICFILES_VENDOR_DIR")
        except AttributeError:
            raise CommandError(
                "STATICFILES_VENDOR_DIR is not defined in settings. "
                "Please add it to your Django settings."
            )

        if not isinstance(vendors_dir, Path):
            vendors_dir = Path(vendors_dir)

        return vendors_dir

    def _display_results(
        self,
        completed_urls: list[str],
        failed_downloads: list[tuple[str, str]],
    ) -> None:
        """Display download results summary.

        Args:
            completed_urls: List of successfully downloaded URLs
            failed_downloads: List of tuples (filename, url) that failed
        """
        self.stdout.write("\n" + "=" * 60)

        total_files = len(VENDOR_STATICFILES)
        success_count = len(completed_urls)
        failed_count = len(failed_downloads)

        if failed_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Successfully downloaded all {total_files} vendor files!"
                )
            )
        elif success_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠ Partial success: {success_count}/{total_files} files downloaded"
                )
            )
            self.stdout.write("\nFailed downloads:")
            for filename, url in failed_downloads:
                self.stdout.write(self.style.ERROR(f"  ✗ {filename}"))
                self.stdout.write(f"    URL: {url}")
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"✗ Failed to download any files ({failed_count} failures)"
                )
            )

        self.stdout.write("=" * 60)
