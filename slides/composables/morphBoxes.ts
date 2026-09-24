// The stream slides arrive from a chat slide by a view transition in which
// the words fly as bare text. The boxes and ids draw only once that morph
// has settled, and fade out again before the deck steps back, so the words
// fly bare in both directions.
import { ref, watch } from "vue";
import { useNav, useSlideContext } from "@slidev/client";
import { beforePrev } from "../stores/leave";

export const MORPH = 1100; // the view transition, from styles/theme.css, plus a beat
export const FADE = 300; // one chip's border and id

export function useMorphBoxes() {
  const { $clicks, $page } = useSlideContext();
  const { currentPage } = useNav();
  const boxed = ref(false);
  let timer: ReturnType<typeof setTimeout> | undefined;

  // Boxes appear once the morph from the previous slide has settled; arriving
  // from anywhere else there is no morph to wait for.
  watch(
    currentPage,
    (now, before) => {
      clearTimeout(timer);
      if (now !== $page.value) {
        boxed.value = false;
        return;
      }
      timer = setTimeout(() => (boxed.value = true), before === $page.value - 1 ? MORPH : 0);
    },
    { immediate: true },
  );

  // Stepping back: fade the boxes out first, then let the deck move.
  watch(
    [currentPage, $clicks],
    () => {
      beforePrev.value =
        currentPage.value === $page.value && $clicks.value === 0
          ? async () => {
              boxed.value = false;
              await new Promise((r) => setTimeout(r, FADE));
            }
          : null;
    },
    { immediate: true },
  );

  return boxed;
}
