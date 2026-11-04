Local text history — development branch

This feature is not included in the published v0.1.0 IPA or the separate branding release build at commit 99b82fd.

Entry point: Settings → VoidGram → Message History. Capture of edits and deletions has separate opt-ins, both off by default. The existing Privacy and Security → VoidGram · Ghost Mode path remains available.

Message context menus also provide VoidGram → Message Details, showing IDs, timestamp, author and thread when available, followed by a link to archive entries filtered to that message. This metadata screen does not copy or re-render message content. Clearing from the filtered screen still asks to clear the entire account archive explicitly.

The previous text is captured immediately before an EditMessage replay replaces it. Text is captured before DeleteMessages and DeleteMessagesWithGlobalIds remove a cached message. The bounded ledger is a PreferencesEntry in the same account's Postbox transaction; rollback also rolls back archive changes. Main chat deletion, read receipts and media removal retain upstream behavior.

Limits: 100 total entries, 8 KB UTF-8 per entry, seven-day retention. Expired records are removed on update replay or opening the archive, rather than by a guaranteed background timer. Oversized texts are skipped without truncation. Repeated identical replay events are deduplicated. This is a bounded archive, not recovery of uncached messages; text containing ordinary webpage previews is eligible.

Media copying is also opt-in and restricted to already-cached photos and files (up to 25 MB per file, 250 MB quota per account), excluded from iCloud backup and protected with iOS file protection until first unlock. Attachments are copied before message deletion and cleaned up when records expire or the archive is cleared. Network downloads are never triggered for archiving.

Formatting entities and reaction/count snapshots now have independent capture controls. Each optional metadata blob is capped at 16 KB; oversized metadata is omitted while eligible text is retained. Formatting-only edits can produce versions when formatting capture is enabled. The detail screen uses Telegram's TextFormat renderer and shows captured reaction summaries (custom reactions display their file ID). Bot-message capture is controlled independently. Old ledger/settings schemas migrate with existing values preserved.

Secret namespaces, copy-protected messages/chats, message auto-remove/auto-clear attributes and ephemeral message attributes are excluded. Chat lifetime must be known and disabled. Unknown chat metadata is skipped. The end of replay and archive reads recheck chat eligibility and remove records for peers that become protected or use auto-removal. No archive leaves the account database. Turning capture off stops new entries; Clear Archive removes existing content after confirmation. Account removal owns database lifetime.

Verification required before release:
- Full native compilation of TelegramCore and SettingsUI (parse-only checks are insufficient).
- Device regression: ordinary private/group/channel text edits and deletions; both cloud deletion paths; repeated replay; text with webpage; missing cached message.
- Exclusion checks: secret chat, protected user/group/channel, unknown cached lifetime, auto-delete enabled, message-specific expiry, all ephemeral variants, media attachments.
- Privacy changes after capture must purge peer records; normal updates, message deletion, media expiration and unread state must still work.
- Account isolation, restart, duplicate events, oldest-entry eviction, seven-day boundary, Clear Archive and settings toggles.
- Native UI: list and detail screens in Russian/English, light/dark modes, large fonts, VoiceOver, records disappearing while details are open. Record and inspect simulator frames per upstream AGENTS.md.

Foundation model tests cover opt-ins, Codable round trip, duplicate events, record identifiers, account/state value isolation, capacity eviction, expiry, targeted purge, Unicode byte limit and clear. They do not establish Postbox or device integration correctness.

## Disappearing media

A separate opt-in in the same block, **Save disappearing media** (`saveDisappearing`, off by default), extends the archive to ephemeral content:

- Chats with an auto-delete timer are archived like ordinary chats while the toggle is on; the timer itself is not modified and the messages still disappear.
- View-once photos, videos and circles are copied from the already cached original in the same Postbox transaction that deletes the ephemeral replacement, before `deleteEphemeralMessages` removes it. The anchor message keeps its media until that point, so the copy is taken from the original, not the empty replacement.
- No chat tombstone is created for view-once messages; the message disappears as usual and the copy is listed in Message History and the Media Archive.
- Archived circles and plain videos get readable labels (`circle.mp4`, `video.mp4`) instead of a generic "attachment".

All existing exclusions still apply: copy-protected content, secret chats, content that was never cached locally, and media the store has already evicted. The toggle participates in the same bounded ledger — 100 records, 8 KB texts, seven-day retention, per-account media quota — and turning it off returns those chats to ordinary exclusion on the next prune.

Device-crash fixes:
- History records encode/decode their event kind as a keyed primitive String. The pinned AdaptedPostboxEncoder and decoder trap in singleValueContainer, which synthesized raw-value enum Codable uses. JSON-only tests missed this path.
- Eligible deleted text now remains in the chat with a registered local AyuDeletedMessageAttribute and a Deleted label beside the time. Secret/expiring/protected content remains excluded. Inline tombstones strip original media and keyboards; captured media stays in the separate bounded archive.
- Repeated deletion replay does not recapture tombstones. Clear, record eviction, expiry and loss of chat eligibility remove retained text. Channel thread counts are decremented once; deleting a tombstone locally does not decrement them again.
- Reply, pin and edit actions are suppressed for retained deleted text in the context menu.
- Before the full app build, ci/test_models.py compiles the exact pinned Postbox Coding.swift, ValueBoxKey.swift (the memory comparator), PostboxLogging.swift, its encoder/decoder helpers and MurMurHash32, then round-trips settings, edited/deleted records and attachment metadata. No database or replica codec is used. The comparator/logger sources are required by Coding.swift; omitting them broke the standalone test compilation. This corrected host check still needs execution on the owner's next manual Codemagic run.
