class Korzina {
    /**
     * Конструктор корзины
     * @param {Element} korzinaDOM - селектор для вставки HTML корзины
     * @param {Element} preloadDOM - селектор для показа и скрытия прелоадера во время загрузки HTML (korzinaDOM)
     * @param {Array of Element} countVarDOM - селекторы для отображения количества товаров в корзине
     * @param {String} nameKeyStorage - название ключа для хранения в LocalStorage
     */
    constructor (korzinaDOM, preloadDOM, countVarDOM, nameKeyStorage = "korzina") {
        this.korzinaDOM = korzinaDOM;
        this.preloadDOM = preloadDOM;
        this.countVarDOM = countVarDOM;
        this.nameKeyStorage = nameKeyStorage;
        this.variacii = []; // массив для храения массива вариаций.
        //this.colichestvo = []; // массив для хранения массива количества вариаций.
        this.LoadFromLocalStorage();
    }
    /**
     * Добавление товара в корзину
     * @param {Int} v - id вариации товара
     * @param {Int} c - количество
     */
    AddTovar(v, c) {
        // ищем в массиве добавляемую вариацию товара
        var b = true;
        for (var i = 0; i < this.variacii.length; i++) {
            if (this.variacii[i].id === v) {
                this.variacii[i].count = parseInt(this.variacii[i].count) + c;
                b = false;
                break;
            }
        }
        if (b) { // если не находим
            this.variacii.push({id: v, count: c}); // добавляем в конец массива
            //this.colichestvo.push(c); // ... за одно и количество :)
        }
        this.SaveToLocalStorage();
    }
    /**
     * Удаление товара из корзины
     * @param {Int} v - id вариации товара
     * @param {Int} c - количество
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
     * Узнаем количество товара в корзине
     * */
    GetCountVars() {
        var r = 0;
        for (var i = 0; i < this.variacii.length; i++) {
            r += parseInt(this.variacii[i].count);
        }
        return r
    }
    /**
     * Показываем на сайте количество товара
     * */
    ShowCount() {
        var count = this.countVarDOM.length;
        var x = this.GetCountVars();
        for (var i = 0; i < count; i++) {
            this.countVarDOM[i].html(x);
        }
    }
    /** 
     *  Полная очистка корзины.
     */
    Clear () {
        this.variacii.length = 0;
        //this.colichestvo.length = 0;
        //this.SaveToLocalStorage();
    }
    Oformit () {
        // Переадресация на страницу оформления заявки.
         
    }
    /** 
     *  Формируем строку для работы с Ajax, JSON и LocalStorage
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
        // Прячем содержимое корзины
        this.preloadDOM.delay(500).fadeIn();
        // Загрузка в объект из локального хранилища
        this.Clear(); // Зачищаем место для новых данных
        this.variacii = JSON.parse(localStorage.getItem(this.nameKeyStorage)); // читаем хранилище
        if (this.variacii === null) {
            this.variacii = [];
        }
        this.preloadDOM.delay(500).fadeOut();
    }
    /**
     * Сохранение набранной корзины в localStorage
     */
    SaveToLocalStorage () {
        // Сохранение в хранилище
        var K = this.variacii; // Получаем строку для сохранения...
        localStorage.setItem(this.nameKeyStorage, JSON.stringify(K)); // Серриализуем в JSON и сохраняем в хранилище.
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
            K.korzinaDOM.html("При загрузке данных произошла ошибка!");
            //alert("Request failed: " + textStatus);
        });
        this.preloadDOM.delay(500).fadeOut();
    }
};