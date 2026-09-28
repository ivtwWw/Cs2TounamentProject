# Changelog

Notable changes to the CS2 Aussie Laozi Cup website and its local management tools are listed chronologically below.

## [v0.0.1] - 2026-09-27
- Established the initial structure of the website.
- Added dynamic match rendering from `matches.json`.
- Recorded the Aussie Laozi Cup S1 match data.
- Reworked `matches.json` and added the initial `README.md` and `changelog.md`.

## [v0.1.0] - 2026-09-28

### Added
- Organized matches by tournament edition, with separate home-page cards and edition pages.
- Added BO3 series overview, per-map navigation, and aggregated player statistics.
- Added champion, captain, MVP, and champion-roster records to completed editions.
- Added FACEIT profile links and player avatars to champion roster entries.
- Added editable edition event-time and schedule fields to the local management menu.
- Added a Hall of Fame home-page card and a dedicated placeholder page.
- Added the ALTV header wordmark, which expands to “Aussie Laozi TV” on hover or keyboard focus.

### Changed
- Reworked the home page to distinguish upcoming editions from completed editions.
- Displayed event time and schedule on home-page edition cards and edition detail pages.
- Removed the “Latest Events” navigation link and simplified edition descriptions when schedule information has been published.
- Aligned match-detail statistic columns to consistent widths across both teams.
- Updated the home-page Hall of Fame placeholder message.
- Documented that MVP Rating is manually entered; it is not calculated by the site.

### Fixed
- Fixed home-page award avatars remaining on their initials fallback instead of loading the FACEIT profile image.
- Improved consistency of award avatars between the home page and edition details.