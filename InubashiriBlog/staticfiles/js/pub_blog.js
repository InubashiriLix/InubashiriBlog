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
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',  // 初始化内容
        config: editorConfig,
        mode: 'default', // or 'simple'
    });

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    });

    $("#blog-form").on("submit", function(event) {
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
            success: function(result){
                if(result['code'] == 200){
                    // 获取博客id并跳转到详情页面
                    let blog_id = result['data']['blog_id'];
                    window.location = '/blog/detail/' + blog_id;
                } else {
                    alert(result['message']);
                }
            }
        });
    });
}
