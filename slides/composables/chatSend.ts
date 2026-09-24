// The chat slides play the exchange when the deck arrives at them from the
// previous slide: the user's message is sent, the assistant types, the reply
// lands. Arriving from anywhere else, by a step back from the token stream
// in particular, the whole exchange is already there, so the morph has its
// targets. Phases: 0 empty, 1 message sent, 2 typing, 3 reply.
import { ref, watch } from "vue";
import { useNav, useSlideContext } from "@slidev/client";

const BEATS = [450, 950, 1700]; // ms after arrival for phases 1, 2, 3, the first after the push settles

export function useChatSend() {
  const { $page } = useSlideContext();
  const { currentPage } = useNav();
  const phase = ref(3);
  let timers: ReturnType<typeof setTimeout>[] = [];

  watch(
    currentPage,
    (now, before) => {
      timers.forEach(clearTimeout);
      timers = [];
      if (now !== $page.value || before !== $page.value - 1) {
        phase.value = 3;
        return;
      }
      phase.value = 0;
      timers = BEATS.map((ms, i) => setTimeout(() => (phase.value = i + 1), ms));
    },
    { immediate: true },
  );

  return phase;
}
