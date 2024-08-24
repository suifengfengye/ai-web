<script setup lang="ts">
import Markdown from 'vue3-markdown-it'
import { computed, ref, watchEffect } from 'vue'

const content = ref(`1233334444`)
const modalInfo = ref({
  visible: true,
  left: 48,
  top: 192 + 48,
  foucsInput: false,
})
const problem = ref('')
const aiAnswer = ref('')
const generating = ref(false)
const castList = ref([
  {
    label: '润色-口语化',
    value: 'polish-口语化',
  },
  {
    label: '润色-更活泼',
    value: 'polish-更活泼',
  },
  {
    label: '润色-更正式',
    value: 'polish-更正式',
  },
  {
    label: '续写',
    value: 'continue_writing',
  },
  {
    label: '缩短篇幅',
    value: 'shorten_text',
  },
  {
    label: '扩充篇幅',
    value: 'expand_text',
  },
])
const contentRef = ref(null)
const inputRef = ref(null)
const conversationId = ref(`c-${Date.now()}`)

const handleMouseRight = (e: any) => {
  modalInfo.value.visible = true;
  modalInfo.value.top = e.pageY;
  if (inputRef?.value) {
    setTimeout(() => {
      inputRef?.value?.focus()
    })
  }
}

const handleClickOutside = () => {
  modalInfo.value.visible = false;
}

const handleSubmit = (params: any, apiKey: string) => {
  // 使用fetch()请求远程的流式API的返回
  generating.value = true;
  fetch(`http://127.0.0.1:8000/${apiKey}/conversationId`, {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({
      ...params,
      engine: 'llama2',
    }),
  })
    .then(response => response.body)
    .then(async (body: any) => {
      // console.log('rb', rb);
      aiAnswer.value = ''
      let reader = body.getReader()
      while (true) {
        let { value, done } = await reader.read()
        // console.log('@@@@value', )
        aiAnswer.value += new TextDecoder().decode(value)
        if (done) {
          console.log('read done')
          generating.value = false;
          break
        }
      }
    })
}

const handleSubmitCustom = () => {
  const text = problem.value
  problem.value = ''
  modalInfo.value.visible = false;
  handleSubmit({
    text: `"${content.value}"。${text}`,
  }, 'ai_stream')
}
const handleBlur = () => {
  setTimeout(() => {
    modalInfo.value.foucsInput = false
  }, 200)
}

const handleClickCast = (item: any) => {
  // console.log('点击了', item)
  const value = item.value
  const [type, sub_type] = value.split('-')
  const params: any = {
    text: content.value,
    type,
  }
  if (sub_type) {
    params.sub_type = sub_type
  }
  // console.log('@@@@@@params', params)
  handleSubmit(params, 'ai_polish')
  modalInfo.value.visible = false;
}

const castVisible = computed(() => {
  return modalInfo?.value?.foucsInput && !problem?.value
})

const loading = ref(true)

const tableData = [
  {
    date: '2016-05-02',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-04',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
  {
    date: '2016-05-01',
    name: 'John Smith',
    address: 'No.1518,  Jinshajiang Road, Putuo District',
  },
]

</script>
<template>
  <div class="doc-box" @contextmenu.prevent="handleMouseRight">
    <p class="doc-content" ref="contentRef">{{ content }}</p>
    <div class="ai-answer-box">
      <span class="loading-span" v-show="generating">loading</span>
      <!-- {{ aiAnswer }} -->
      <Markdown :source="aiAnswer" />
    </div>
    <div class="modal-box" :style="{
    display: modalInfo?.visible ? '' : 'none',
    // top: `${modalInfo.top}px`,
    // left: `${modalInfo.left}px`
  }" v-click-outside="handleClickOutside">
      <div class="input-box">
        <span class="input-box-icon">-></span>
        <input v-model="problem" ref="inputRef" @keydown.enter="handleSubmitCustom" placeholder="输入问题，或从下方选择场景提问。"
          @focus="modalInfo.foucsInput = true" @blur="handleBlur" />
        <span class="send-btn" :class="[problem ? 'active' : '']" @click="handleSubmitCustom">发送</span>
      </div>
      <div class="cast-list-box" v-show="castVisible">
        <ul>
          <li v-for="item in castList" :key="item.value" @click="handleClickCast(item)">
            {{ item.label }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped lang="less">
.doc-box {
  position: relative;
  width: 1000px;
  min-height: 1000px;
  margin: 0 auto;
  padding: 48px;
  background-color: #fff;

  .doc-content {
    white-space: pre-wrap;
  }
}

.modal-box {
  position: relative;
  // position: absolute;
  // top: 192px + 48px;
  // left: 48px;
  width: 904px;
  margin-top: 24px;

  .input-box {
    display: flex;
    width: 100%;
    height: 48px;
    // padding-left: 40px;
    background-color: #000;
    border-radius: 8px;

    .input-box-icon {
      color: #fff;
      padding: 0 12px;
      line-height: 46px;
    }

    .send-btn {
      color: #767676;
      padding: 0 12px;
      line-height: 46px;
      cursor: pointer;

      &.active {
        color: #fff;
      }
    }

    input {
      flex: 1 auto;
      background-color: #000;
      border: none;
      outline: none;
      color: #fff;
      font-size: 16px;
    }
  }
}

.ai-answer-box {
  position: relative;
  border: 2px solid slateblue;
  border-radius: 8px;
  padding: 12px 20px;
  margin-top: 16px;

  .loading-span {
    position: absolute;
    top: -1px;
    left: 4px;
    background: #ccc;
    line-height: 14px;
    border-radius: 4px;
  }
}

.cast-list-box {
  position: absolute;
  top: 42px;
  left: 38px;
  padding: 12px 6px;
  background-color: lighten(#000, 20%);
  border-radius: 4px;
  color: #fff;

  ul {
    list-style: none;
    padding: 0;

    li {
      padding: 0 12px;
      line-height: 32px;
      border-radius: 4px;
      cursor: pointer;

      &:hover {
        background-color: #767676;
      }
    }
  }
}
</style>
