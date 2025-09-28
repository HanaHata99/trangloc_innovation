function sayHello() {
    alert("Hello from JavaScript!");
}

window.onload = () => {
    let figureLoading = document.querySelector('#figure-container > div');

    window.addEventListener("message", (event) => {
        if (event.data && event.data.frameHeight) {
            const iframe = document.getElementById("figure-frame");
            const padding = 50;
            iframe.style.height = (event.data.frameHeight + padding) + "px";
            figureLoading.classList.add("d-none");
            figureLoading.classList.remove("d-flex");
        }
    });

    let min_rms = 0.02;
    let txt_min_rms = document.getElementById('min_rms');
    let txtReference = document.getElementById('txtReference');

    let getSettingAjax = new Ajax('/get_settings', resp => {
        data = JSON.parse(resp);
        min_rms = data.min_rms;
        console.log(`Giá trị ngưỡng tối thiểu: ${min_rms}`);
        txt_min_rms.value = min_rms;
    });
    getSettingAjax.request();

    var settingModal = document.getElementById('settingModal');
    settingModal.addEventListener('hide.bs.modal', function (event) {
        txt_min_rms.value = min_rms;
        console.log('Đóng popup');
    });

    const btnUpdateSetting = document.getElementById('btnUpdateSetting');
    btnUpdateSetting.onclick = () => {
        min_rms = txt_min_rms.value;
        fetch('/update_settings', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "min_rms": min_rms })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

        var modalInstance = bootstrap.Modal.getInstance(settingModal);
        modalInstance.hide();
    };

    const btnCompute = document.getElementById('btnCompute');
    btnCompute.onclick = () => {
        reference = txtReference.value;
        fetch('/compute_eed', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "reference": reference })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
        var modalInstance = bootstrap.Modal.getInstance(settingModal);
        modalInstance.hide();
    };

    const btnReload = document.getElementById('btnReload');
    btnReload.onclick = () => {
        location.reload();
    }

    const btnPause = document.getElementById('btnPause');
    btnPause.onclick = () => {
        fetch('/pause_resume', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "state": btnPause.innerText})
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

        if ('Tạm dừng' == btnPause.innerText) {
            btnPause.innerText = 'Tiếp tục'
        } else {
            btnPause.innerText = 'Tạm dừng'
        }
    }

    const camxuc = document.getElementById('camxuc')
    let camxucAjax = new Ajax('/camxuc', resp => {
        // console.log(`Giá trị cảm xúc: ${resp}`);
        if ('Invalid' === resp) {

        } else {
            camxuc.value = resp;
        }
    });
    camxucAjax.request(500);

    const cadaotucngu = document.getElementById('cadaotucngu')
    let cadaotucnguAjax = new Ajax('/cadaotucngu', resp => {
        // console.log(`Giá trị ca dao tục ngữ: ${resp}`);
        if ('Invalid' === resp) {

        } else {
            cadaotucngu.value = resp;
        }
    });
    cadaotucnguAjax.request(500);
}
