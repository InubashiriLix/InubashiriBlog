console.log("pub_blog.js is loaded and running.");

window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor;

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml();
            console.log('editor content', html);
            // 每次编辑器内容变化时，手动同步编辑器内容到隐藏的 <textarea>
            document.querySelector("#content-textarea").value = html;
        },
        // 添加菜单项以支持代码块
        menus: [
            'head', 'bold', 'italic', 'underline', 'strikeThrough', 'justify', 'quote', 'image', 'link', 'list', 'code', 'undo', 'redo'
        ],
        // 在插入代码时确保用 <pre><code> 包裹
        customInsert: (insertCodeFn) => {
            // 自定义插入代码的逻辑
            const codeHtml = '<pre><code class="language-python"># your code here</code></pre>';
            insertCodeFn(codeHtml);  // 将代码插入编辑器
        },
        // 在插入粘贴的内容时保持缩进和换行
        pasteFilterStyle: false,  // 保留粘贴的原始格式和样式
        showFullScreen: true,     // 启用全屏模式，方便代码编辑
    };

    // 初始化编辑器
    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',  // 初始化内容为空
        config: editorConfig,
        mode: 'default', // 可以使用 'simple' 模式
    });

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    });

    $("#submit-btn").click(function (event) {
        console.log("Clicked submit button.");
        // 阻止表单的默认提交行为
        event.preventDefault();
        console.log("Submitting form...");

        let content = editor.getHtml();
        document.querySelector("#content-textarea").value = content;
        console.log('Content before submit:', content);  // 调试输出

        // 使用 serialize() 提交表单所有字段
        let formData = $("form").serialize();
        console.log('Serialized form data:', formData);  // 打印序列化的表单数据

        $.ajax('/blog/pub', {
            method: 'POST',
            data: formData,  // 使用序列化的表单数据
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
            },
            success: function(result){
                if(result['code'] == 200){
                    // 获取博客id
                    let blog_id = result['data']['blog_id']
                    // 跳转到博客详情页面
                    window.location = '/blog/detail/' + blog_id
                }else{
                    alert(result['message']);
                }
            },
            error: function (xhr, status, error) {
                // 错误处理
            }
        });
    });

}
