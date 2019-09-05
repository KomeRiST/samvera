class Korzina {
    /**
     * ����������� �������
     * @param {Element} korzinaDOM - �������� ��� ������� HTML �������
     * @param {Element} preloadDOM - �������� ��� ������ � ������� ���������� �� ����� �������� HTML (korzinaDOM)
     * @param {Array of Element} countVarDOM - ��������� ��� ����������� ���������� ������� � �������
     * @param {String} nameKeyStorage - �������� ����� ��� �������� � LocalStorage
     */
    constructor (korzinaDOM, preloadDOM, countVarDOM, nameKeyStorage = "korzina") {
        this.korzinaDOM = korzinaDOM;
        this.preloadDOM = preloadDOM;
        this.countVarDOM = countVarDOM;
        this.nameKeyStorage = nameKeyStorage;
        this.variacii = []; // ������ ��� ������� ������� ��������.
        //this.colichestvo = []; // ������ ��� �������� ������� ���������� ��������.
        this.LoadFromLocalStorage();
    }
    /**
     * ���������� ������ � �������
     * @param {Int} v - id �������� ������
     * @param {Int} c - ����������
     */
    AddTovar(v, c) {
        // ���� � ������� ����������� �������� ������
        var b = true;
        for (var i = 0; i < this.variacii.length; i++) {
            if (this.variacii[i].id === v) {
                this.variacii[i].count = parseInt(this.variacii[i].count) + c;
                b = false;
                break;
            }
        }
        if (b) { // ���� �� �������
            this.variacii.push({id: v, count: c}); // ��������� � ����� �������
            //this.colichestvo.push(c); // ... �� ���� � ���������� :)
        }
        this.SaveToLocalStorage();
    }
    /**
     * �������� ������ �� �������
     * @param {Int} v - id �������� ������
     * @param {Int} c - ����������
     */
    DelTovar (v, c = 1) {
        for (var i = this.variacii.length-1; i >= 0; i--) {
            if (this.variacii[i].id === v) {
                this.variacii.splice(i, i);
                break;
            }
        }
        this.SaveToLocalStorage();
    }
    /**
     * ������ ���������� ������ � �������
     * */
    GetCountVars() {
        var r = 0;
        for (var i = 0; i < this.variacii.length; i++) {
            r += parseInt(this.variacii[i].count);
        }
        return r
    }
    /**
     * ���������� �� ����� ���������� ������
     * */
    ShowCount() {
        var count = this.countVarDOM.length;
        var x = this.GetCountVars();
        for (var i = 0; i < count; i++) {
            this.countVarDOM[i].html(x);
        }
    }
    /** 
     *  ������ ������� �������.
     */
    Clear () {
        this.variacii.length = 0;
        //this.colichestvo.length = 0;
        //this.SaveToLocalStorage();
    }
    Oformit () {
        // ������������� �� �������� ���������� ������.
         
    }
    /** 
     *  ��������� ������ ��� ������ � Ajax, JSON � LocalStorage
     */
    GetString() {
        if (this.variacii.length < 1) {
            return null;
        } else {
            var v = "";
            var c = "";
            var x = this.variacii.length;
            for (var i = 0; i < x; i++) {
                v = v + this.variacii[i].id;
                c = c + this.variacii[i].count;
                if (i < (x-1)) {
                    v = v + ',';
                    c = c + ',';
                }
            }
            return v + '|' + c
        }
    }
    LoadFromLocalStorage () {
        // ������ ���������� �������
        this.preloadDOM.delay(500).fadeIn();
        // �������� � ������ �� ���������� ���������
        this.Clear(); // �������� ����� ��� ����� ������
        this.variacii = JSON.parse(localStorage.getItem(this.nameKeyStorage)); // ������ ���������
        if (this.variacii === null) {
            this.variacii = [];
        }
        this.preloadDOM.delay(500).fadeOut();
    }
    /**
     * ���������� ��������� ������� � localStorage
     */
    SaveToLocalStorage () {
        // ���������� � ���������
        var K = this.variacii; // �������� ������ ��� ����������...
        localStorage.setItem(this.nameKeyStorage, JSON.stringify(K)); // ������������ � JSON � ��������� � ���������.
        this.ShowCount();
    }
    KorzinaGet() {
        var K = this;
        var request = $.ajax({
            url: "/korzinaget/",
            method: "get",
            //contentType: 'application/json; charset=utf-8',
            data: { korzina: this.GetString() },
            dataType: 'text',
        });

        request.done(function (msg) {
            K.korzinaDOM.html(msg);
            //localStorage.removeItem("korzina");
            //j = $("#kor").html();
            //j = JSON.parse(j);
            //localStorage.setItem("korzina", JSON.stringify(j));
            //$("#kor").remove();
        });

        request.fail(function (jqXHR, textStatus) {
            K.korzinaDOM.html("��� �������� ������ ��������� ������!");
            //alert("Request failed: " + textStatus);
        });
        this.preloadDOM.delay(500).fadeOut();
    }
};