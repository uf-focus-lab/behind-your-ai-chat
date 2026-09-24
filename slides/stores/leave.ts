// A page may ask for a moment before the deck steps back from it: the token
// stream fades its boxes out, and only then does the view transition carry
// the words back into the chat bubbles. The page registers the wait while it
// is the one a "previous" keypress would leave.
import { ref } from "vue";

export const beforePrev = ref<null | (() => Promise<void>)>(null);

export async function prevAfterLeave(prev: () => void) {
  if (beforePrev.value) await beforePrev.value();
  prev();
}
