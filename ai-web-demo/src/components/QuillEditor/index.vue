<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.core.css'
import "quill/dist/quill.snow.css";

const Delta = Quill.import('delta')

// props
const props = defineProps<{ 
  id: string,
  content: string,
  classList: string[]
 }>()

//  emit
const emit = defineEmits(['on-change', 'on-dblclick'])

// refs
const editorContainerRef: any = ref(null)

// state

// quill editor
let quillInst: any = null
let currentSelection: any = null

// ref
defineExpose({
  clearFormat: () => {
    if (currentSelection) {
      quillInst.removeFormat(currentSelection.index, currentSelection.length, 'user');
      currentSelection = null
    }
  },
  getText: () => {
    if (currentSelection) {
      return quillInst.getText(currentSelection.index, currentSelection.length)
    }
    // return quillInst.getText()
    return ''
  },
  replace: (text: string) => {
    if (!currentSelection) {
      return
    }
    const _update = new Delta()
    .retain(currentSelection.index)
    .delete(currentSelection.length)
    .insert(text)
    quillInst.updateContents(_update)
  },
  insert: (text: string) => {
    if (!currentSelection) {
      return
    }
    const _update = new Delta()
    .retain(currentSelection.index + currentSelection.length)
    .insert('\n\n')
    .insert(text)
    .insert('\n\n')
    quillInst.updateContents(_update)
  },
  getQuillInst: () => {
    return quillInst
  },
  getEditor: () => {
    return editorContainerRef?.value
  },
})

onMounted(() => {
  quillInst = new Quill(editorContainerRef.value, {
    theme: 'snow',
    placeholder: '输入问题，或从下方选择场景提问。',
  })
  if (props.content) {
    quillInst.setText(props.content)
  }



  quillInst.on('text-change', (delta: typeof Delta, oldDelta: typeof Delta, source: string) => {
    emit('on-change', { content: quillInst.getText(), delta, oldDelta, source })
  })

  // 监听右键事件
  editorContainerRef.value.addEventListener('contextmenu', async (event: Event) => {
    event.preventDefault();
    if (currentSelection) {
      quillInst.removeFormat(currentSelection.index, currentSelection.length, 'user');
    }
    currentSelection = quillInst.getSelection();
    emit('on-dblclick', event)
    if (currentSelection && currentSelection.length > 0) {
      // 应用高亮样式
      quillInst.formatText(currentSelection.index, currentSelection.length, {
          'background-color': '#d0eac8' // 使用内联样式直接设置背景色
      }, 'user');
    }
  });
})

watch(() => props.content, (newValue) => {
  quillInst.setText(newValue)
})
</script>
<template>
<div class="quill-core-wrapper">
  <div ref="editorContainerRef" :id="props.id || ''" :class="props.classList || []"></div>
</div>
</template>
<style lang="less">
@doc-width: 960px;
.quill-core-wrapper {
  .ql-container {
    width: @doc-width;
    margin: 0 auto 24px;
    box-shadow: rgba(0, 0, 0, 0.06) 0px 0px 10px 0px, rgba(0, 0, 0, 0.04) 0px 0px 0px 1px;
    border: none;
    background: #fff;
    font-size: 14px;
  }

  .ql-toolbar.ql-snow {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: #f9fafb;
  }
}
</style>
