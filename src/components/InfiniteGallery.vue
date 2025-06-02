<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  initialItems: { type: Array, required: true },   // full list
});

const batchSize = 30;
const visible   = ref(props.initialItems.slice(0, batchSize));

function showNext() {
  const next = props.initialItems.slice(
    visible.value.length,
    visible.value.length + batchSize
  );
  if (next.length) visible.value.push(...next);
}

function observe(lastEl) {
  if (!lastEl) return;
  const io = new IntersectionObserver(([e]) => {
    if (e.isIntersecting) {
      io.disconnect();
      showNext();
    }
  }, { threshold: 0.5 });
  io.observe(lastEl);
}

onMounted(() => {
  watch(visible, () => {
    observe(document.querySelector('#gallery li:last-child'));
  }, { flush: 'post' });
});
</script>

<template>
  <!-- 1-col mobile, 3-col desktop, 1px gaps -->
  <ul id="gallery" class="grid gap-px grid-cols-1 md:grid-cols-3">
    <li v-for="(item, i) in visible" :key="i">
      <component :is="item.type === 'video' ? 'video' : 'img'"
                 :src="item.src"
                 :alt="item.alt"
                 class="w-full h-auto"
                 v-bind="item.type === 'video'
                   ? { muted:true, autoplay:true, loop:true, playsinline:true }
                   : { loading:'lazy' }" />
    </li>
  </ul>
</template>