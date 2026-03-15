// "写一个函数，把嵌套的列表拍平成一维列表。"

// ```
// 输入：[1, [2, [3, 4], 5], 6]
// 输出：[1, 2, 3, 4, 5, 6]
// ```

function flattern(nums) {
    let result = []
    for (let i = 0, len = nums.length; i < len; i++) {
        if (Array.isArray(nums[i])) {
            const _tmp = flattern(nums[i])
            result = [...result, ..._tmp]
        } else {
            result.push(nums[i])
        }
    }
    return result
}
// const _arr = [1, [2, [3, 4], 5], 6]
// console.log(flattern(_arr))

// "现在不是列表了，是嵌套字典。把它拍平，key 用点号连接。"

// ```
// 输入：{"a": {"b": 1, "c": {"d": 2}}, "e": 3}
// 输出：{"a.b": 1, "a.c.d": 2, "e": 3}
// ```
function flatternDict(objArg) {
    const resultObj = {}
    const innerFn = (obj, parentKey, resultObj) => {
        Object.entries(obj).forEach(([key, value]) => {
            const tmpKey = parentKey ? `${parentKey}.${key}` : key
            if (typeof value === 'object') {
                innerFn(value, tmpKey, resultObj)
            } else {
                resultObj[tmpKey] = value
            }
        })    
    }
    innerFn(objArg, '', resultObj)
    return resultObj
}
// const _obj = {"a": {"b": 1, "c": {"d": 2}}, "e": 3}
// console.log(flatternDict(_obj))

// 输入：{"a": {"b": 1, "c": {"d": 2}}, "e": 3}
// 输出：{"a.b": 1, "a.c.d": 2, "e": 3}

function revertFlatternDict(objArg){
    const resultObj = {}
    Object.entries(objArg).forEach(([key, value]) => {
        if (key.includes('.')) {
            const keyList = key.split('.')
            let tmpObj = resultObj
            keyList.forEach((keyItem, index) => {
                if (index === keyList.length - 1) {
                    tmpObj[keyItem] = value
                } else {
                    if (!tmpObj[keyItem]) {
                        tmpObj[keyItem] = {}
                    }
                    tmpObj = tmpObj[keyItem]
                }
            })
        } else {
            resultObj[key] = value
        }
    })
    return resultObj
}
const flatternObj = {"a.b": 1, "a.c.d": 2, "e": 3}
console.log(revertFlatternDict(flatternObj))