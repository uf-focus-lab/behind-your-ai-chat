// Keyboard navigation, with one addition: a page may ask for a moment before
// the deck steps back from it (stores/leave.ts), so the token-stream slides
// can fade their boxes out before the words fly back into the chat window.
import { defineShortcutsSetup } from "@slidev/types";
import type { NavOperations, ShortcutOptions } from "@slidev/types";
import { prevAfterLeave } from "../stores/leave";

export default defineShortcutsSetup(
  (nav: NavOperations, base: ShortcutOptions[]) => {
    const prev = new Set(["prev_left", "prev_space"]);
    return base.map((shortcut) =>
      prev.has(shortcut.name!)
        ? { ...shortcut, fn: () => void prevAfterLeave(() => void nav.prev()) }
        : shortcut,
    );
  },
);
