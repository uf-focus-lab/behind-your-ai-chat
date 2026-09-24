<script setup lang="ts">
// A chat app window in the manner of a macOS app: traffic lights, a centred
// title, one user bubble, one assistant bubble with a generic AI mark, and
// an input field. The pages put their tokens in the two slots so the words
// keep their view-transition names; `phase` plays the send (see
// composables/chatSend.ts): 0 empty, 1 message sent, 2 typing, 3 reply.
//
//   <ChatWindow :phase="phase" height="396px" typing-vt="tok-a-typing">
//     <template #user>…token spans…</template>
//     <template #agent>…token spans…</template>
//   </ChatWindow>
withDefaults(defineProps<{ phase?: number; height?: string; typingVt?: string }>(), {
  phase: 3,
  height: '396px',
  typingVt: undefined,
})
</script>

<template>
  <div class="chat" :class="`phase-${phase}`" :style="{ height }">
    <header class="chat-bar">
      <span class="chat-lights" aria-hidden="true"><i /><i /><i /></span>
      <span class="chat-title">Your Favourite AI Chatbot</span>
    </header>
    <div class="chat-body">
      <div class="chat-msg user">
        <div class="chat-bubble"><slot name="user" /></div>
      </div>
      <div class="chat-msg agent">
        <span class="chat-mark" aria-hidden="true">✦</span>
        <div v-if="phase >= 3" class="chat-bubble"><slot name="agent" /></div>
        <div v-else class="chat-bubble chat-typing" :style="typingVt ? { viewTransitionName: typingVt } : undefined"><i /><i /><i /></div>
      </div>
    </div>
    <footer class="chat-input">Message your favourite AI chatbot</footer>
  </div>
</template>

<style scoped>
/* Geometry: the corner radius --r is also the red light's centre offset
   from the window's top and left edges, so the light and the corner arc
   share a centre. The lights are placed by their centre, not by flex
   centring, and the 1px border is subtracted since it sits inside the
   radius. The title bar is 2 --r tall so the lights are centred in it. */
.chat {
  --r: 22px;
  --light: 12px;
  width: 680px;
  display: flex;
  flex-direction: column;
  border: 1px solid color-mix(in srgb, var(--ink-strong) 14%, transparent);
  border-radius: var(--r);
  overflow: hidden;
  background: var(--paper);
  box-shadow: 0 18px 48px -12px rgba(0, 0, 0, 0.28), 0 2px 6px rgba(0, 0, 0, 0.1);
}
.dark .chat { box-shadow: 0 18px 48px -12px rgba(0, 0, 0, 0.7), 0 2px 6px rgba(0, 0, 0, 0.4); }
.chat-bar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(2 * var(--r));
  border-bottom: 1px solid var(--ink-hair);
  background: color-mix(in srgb, var(--ink-hair) 40%, var(--paper));
}
.chat-lights { position: absolute; top: calc(var(--r) - var(--light) / 2 - 1px); left: calc(var(--r) - var(--light) / 2 - 1px); display: flex; gap: 8px; }
.chat-lights i { width: var(--light); height: var(--light); border-radius: 50%; }
.chat-lights i:nth-child(1) { background: #ff5f57; }
.chat-lights i:nth-child(2) { background: #febc2e; }
.chat-lights i:nth-child(3) { background: #28c840; }
.chat-title { font-size: 16px; font-weight: 600; color: var(--ink); }
.chat-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 1.4rem;
}
.chat-msg { display: flex; align-items: flex-end; gap: 0.7rem; transition: opacity 0.35s ease, transform 0.35s ease; }
/* the send: the message rises into place, then the assistant appears */
.phase-0 .chat-msg.user { opacity: 0; transform: translateY(14px); }
.phase-0 .chat-msg.agent, .phase-1 .chat-msg.agent { opacity: 0; }
.chat-msg.user { justify-content: flex-end; }
.chat-mark {
  flex: none;
  width: 28px; height: 28px;
  margin-bottom: 4px;
  border-radius: 8px;
  background: var(--ink-strong);
  color: var(--paper);
  font-size: 17px;
  line-height: 28px;
  text-align: center;
}
.chat-bubble {
  max-width: var(--chat-bubble-w, 470px);
  padding: 0.65rem 1.05rem;
  border-radius: 18px;
  font-size: 21px;
  line-height: 1.4;
  color: var(--ink-strong);
  white-space: pre-wrap;
}
.user .chat-bubble { background: color-mix(in srgb, var(--ink-hair) 45%, var(--paper)); border-bottom-right-radius: 6px; }
.agent .chat-bubble { border: 1px solid var(--ink-hair); border-bottom-left-radius: 6px; }
.chat-typing { display: flex; gap: 6px; align-items: center; padding: 0.95rem 1.1rem; }
.chat-typing i { width: 9px; height: 9px; border-radius: 50%; background: var(--ink-dim); animation: chat-blink 1.2s infinite ease-in-out; }
.chat-typing i:nth-child(2) { animation-delay: 0.2s; }
.chat-typing i:nth-child(3) { animation-delay: 0.4s; }
@keyframes chat-blink { 0%, 80%, 100% { opacity: 0.25; } 40% { opacity: 1; } }
.chat-input {
  margin: 0 1.4rem 1.1rem;
  padding: 0.55rem 1.1rem;
  border: 1px solid var(--ink-hair);
  border-radius: 22px;
  font-size: 16px;
  color: var(--ink-dim);
}
</style>
