export function getElementLeft (element: any, parentClassName?: string) {
  if (!element) {
    return 0
  }
  let actualLeft = element.offsetLeft
  let current = element.offsetParent
  let className = current ? current.className : ''
  while ((current !== null && current !== undefined) && (!className || className.indexOf(parentClassName) === -1)) {
    if (current.offsetLeft !== undefined) {
      actualLeft += current.offsetLeft
    }
    current = current.offsetParent
    if (current) {
      className = current.className
    } else {
      className = ''
    }
  }
  return actualLeft
}

type EventListener = (event: Event) => void;

export const EventUtil = {
  // 跨浏览器获取 event 对象
  getEvent (event: Event) {
    return event || window.event
  },

  // 跨浏览器获取 target 属性
  getTarget (event: Event) {
    return event.target || event.srcElement
  },

  // 阻止事件的默认行为
  preventDefault (event: Event) {
    if (event.preventDefault) {
      event.preventDefault()
    } else {
      event.returnValue = false
    }
  },

  // 阻止事件流或使用 cancelBubble
  stopPropagation (event: Event) {
    if (event.stopPropagation) {
      event.stopPropagation()
    } else {
      event.cancelBubble = true
    }
  },

  //  判断点击是否是否点击的classNames下的子元素
  isClickChildren ({ event, classNames, id }: { event: Event, classNames?: string[], id?: string }): boolean {
    // 判断eventTarget是否是不允许关闭的节点
    const target: any = event.target
    let parent: any = target
    let isContain = false

    // // svg图标，root元素为svg，不会再往上遍历到html元素中；所以点击svg图标时，parent取事件路径数组中的下一个不是svg类的元素
    // if (['path', 'svg'].indexOf(parent.nodeName) !== -1 && event.path && event.path.length > 0) {
    //   for (let i = 0, len = event.path.length; i < len; i++) {
    //     if (['path', 'svg'].indexOf(event.path[i].nodeName) === -1) {
    //       parent = event.path[i]
    //       break
    //     }
    //   }
    // }

    // 防止冒泡的处理（由于合成事件和原生事件的存在，处理较复杂）
    // 这里采用target判断的方式，写起来繁琐，但是比较解耦
    // const notCloseBox = ['ev-stop-dropdown', 'persons-select-dropdown-box']
    const foundBox = (className: string, eleId: string) => {
      let isBox = false
      for (let i = 0, len = classNames.length; i < len; i++) {
        if (className && className.indexOf && className.indexOf(classNames[i]) !== -1) {
          isBox = true
          break
        }
        if (eleId === id) {
          isBox = true
          break
        }
      }
      return isBox
    }

    while (parent) {
      const className = parent.className
      const eleId = parent.id
      if ((className || eleId) && foundBox(className, eleId)) {
        isContain = true
        break
      }
      parent = parent.parentNode
    }
    return isContain
  },
}
