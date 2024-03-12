<script setup lang="ts">
import Markdown from 'vue3-markdown-it'
import { computed, ref, watchEffect } from 'vue';

const content = ref(`小文盲在班里是学习最差的，整天像这假期该怎么玩，作业没有一天写完过。新学期又开始了，他背着仿佛千斤重的书包，在回家的路上。
      
忽然，他看见一个卖茶叶蛋的小摊。他克服不了见什么食物都馋的毛病，用妈妈给他买本子的两块钱买了四个茶叶蛋，刚放到嘴里，又念一想：我何必不开个卖茶叶蛋的小摊呢？这样既能赚钱，又能吃到自己爱吃的茶叶蛋，这不是两全其美吗？说干就干，他向妈妈要了1000元说要交学费，然后自己开了个卖茶叶蛋的小摊。花200元买了个炉子，写了个招牌，靠平时观察别人做茶叶蛋的方法做了起来，然后把课本当柴烧，扔进了炉子里。那个体营业证怎么办呢？他花高价请路人写了个个体营业证，挂在自己营业后面的墙上，还贴了张自己的照片。`)
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
  fetch(`http://127.0.0.1:8000/${apiKey}`, {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(params),
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
  }, 'ai_fixed_content_custom')
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
  handleSubmit(params, 'ai_fixed_content')
  modalInfo.value.visible = false;
}

const castVisible = computed(() => {
  return modalInfo?.value?.foucsInput && !problem?.value
})
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
