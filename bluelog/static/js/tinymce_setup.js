tinymce.init({
    //选择class为content的标签作为编辑器
    selector: '#content',
    //方向从左到右
    directionality:'ltr',
    //语言选择中文
    //高度为400
    height:400,
    images_upload_url: 'https://graph.baidu.com/upload',
    images_upload_base_path: 'uploads',
	image_title: true,
	image_caption: true,

    //工具栏上面的补丁按钮


    plugins: [
        'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
        'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
        'save table contextmenu directionality emoticons template paste textcolor',  'image', 'imagetools',
        'codesample', "image code preview", "code","wordcount",
    ],
    //工具栏的补丁按钮
    toolbar: 'insertfile undo redo | \
     styleselect | \
     bold italic | \
     alignleft aligncenter alignright alignjustify | \
     bullist numlist outdent indent | \
     image | \
     code | \
     wordcount | \
     print preview media fullpage | \
     forecolor backcolor emoticons |\
     codesample fontsizeselect fullscreen',



    //字体大小
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
    //按tab不换行
    nonbreaking_force_tab: true,
    automatic_uploads: false,
			paste_data_images: true,
			images_upload_handler: this.imgUpload,

    codesample_languages: [
        {text: 'HTML/XML', value: 'markup'},
        {text: 'JavaScript', value: 'javascript'},
        {text: 'CSS', value: 'css'},
        {text: 'PHP', value: 'php'},
        {text: 'Python', value: 'python'},
    ],
    codesample_content_css: '/static/prism.css',


    imgUpload (blobInfo, success, failure) {
			const formData = new FormData();
			formData.append('files', blobInfo.blob(), blobInfo.filename());
			axios.post('/api/file/post', formData).then((res) => {
				if(res.data.success) {
					this.$message({
						message: '上传成功',
						type: 'success',
						center: true
					});
					let url = res.data.urls[0].url
					this.imgString += url
					success(url)
				} else {
					this.$message({
						message: '上传失败',
						type: 'error',
						center: true
					});
					failure('')
				}
			}).catch((err) => {
				this.$message({
					message: '上传失败',
					type: 'error',
					center: true
				});
				failure('')
            })
		},

});
