
"use strict";
console.log(result_id);

// 获取用户id
const e_uid = document.cookie.split(';')[1].trim().split('=')[1];
var storage = window.localStorage;
console.log(storage.getItem(e_uid));
// 判断是否存在
function justData(record_id, arr) {
    for (let x = 0; x < arr.length; x++) {
        // 判断问题id 是否存在
        if (arr[x].test_record_id === record_id) {
            return x;
        }
    }
    return -1
}

// 翻页事件
function go() {
    let href = $node("go").getAttribute('href');
    let options = document.getElementsByClassName('options');
    let arr = [];
    if(storage.getItem(e_uid)){
        arr = JSON.parse(storage.getItem(e_uid));
    }
    for(let i=0; i<options.length; i++){
        if(options[i].checked){
            let preNode = options[i].parentNode.parentNode.parentNode;
            let preNode1 = preNode.previousElementSibling; // 获取父节点的上一个兄弟节点
            let preNode2 = preNode1.previousElementSibling; // 获取兄弟节点
            let record = preNode2.children; // 获取子节点
            let record_id = record[0].value;
            let opts = [];
            // 如果数组为空 直接添加
            if(!arr.length){
                opts.push(options[i].value);
                let dic = {
                    "test_record_id": record_id,
                    "opts": opts,
                };
                arr.push(dic);
                continue
            }

            let result = justData(record_id, arr);
            if(result !== -1){
                if(arr[result].opts.indexOf(options[i].value)===-1){
                    arr[result].opts.push(options[i].value);
                }
            }else{
                    opts.push(options[i].value);
                    let dic = {
                        "test_record_id": record_id,
                        "opts": opts,
                    };
                    arr.push(dic);
                }
            }else{

                if(!arr){
                    return
                }

                arr.forEach(function (v,k) {
                    if(v.opts.indexOf(options[i].value)!==-1){
                        // 对象数组长度大于1 删除对象数组中某个元素 否则删除对象数组
                        if(v.opts.length>1){
                            let index = v.opts.indexOf(options[i].value);
                            v.opts.splice(index, 1);
                        }else{
                            arr.splice(k, 1)
                        }
                    }
                })
        }
        }

        storage.setItem(e_uid, JSON.stringify(arr));  // 存储到本地
}

// 加载时判断题是否选中
window.onload = function () {
    let arr = [];
    if(storage.getItem(e_uid)){
        arr = JSON.parse(storage.getItem(e_uid));
    }
    if(!arr){
        return
    }
    let options = document.getElementsByClassName('options');
    for(let i=0; i<options.length; i++){
        arr.forEach(function (v,k) {
            if(v.opts.indexOf(options[i].value)!==-1){
                options[i].checked = true;
                return
            }
        })
    }
};

// 提交事件
$node("form_box").onsubmit = function () {
    go(); //调用go;
    let url = $node("form_box").getAttribute('action');
    console.log(url);
    $node("opts").value = storage.getItem(e_uid);
    // $("form_box").setAttribute('action', url);
    storage.removeItem(e_uid);
    return true
};