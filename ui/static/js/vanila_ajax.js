class Ajax {
    constructor(url, callback, method='GET') {
        const self = this;
        this.url = url
        this.method = method;
        this.callback = callback;
        this.intervalId = null;
        this.readyToSend = true;

        this.xhttp = new XMLHttpRequest();
        this.xhttp.onload = function() {
            self.onResponse(this.responseText);
        }
        this.xhttp.onreadystatechange = function() {
            self.onReadyStateChanged(this.readyState, this.status);
        };
    }

    private_send() {
        this.readyToSend = false;
        this.xhttp.open(this.method, this.url);
        this.xhttp.send();
    }

    request(interval) {
        if (interval) {
            this.intervalId = setInterval((ajax) => {
                if (true === ajax.readyToSend) {
                    ajax.private_send();
                } else {
                    console.warn('Cần phải đợi request trước đó hoàn thành');
                }
            }, interval, this)
        } else {
            this.private_send();
        }
    }

    stop() {
        if (null !== this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    onReadyStateChanged(readyState, status) {
        if (4 === readyState) {
            this.readyToSend = true;
        }
    }

    onResponse(resp) {
        if (null !== this.callback) {
            this.callback(resp);
        }
    }
}