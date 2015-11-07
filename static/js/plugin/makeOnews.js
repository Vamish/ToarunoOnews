$.fn.makeONEWS = function (data) {
    var self = this;
    self.empty();

    $.each(data, function (i) {
        var listItem = document.createElement('li');
        $(listItem).addClass('onews');
        $(listItem).attr('data-newsid', data[i].id);

        var img = document.createElement('img');
        $(img).attr('src', data[i].title_img);

        var header = document.createElement('header');
        var h2 = document.createElement('h2');
        var time = new Date(data[i].time);
        var year = time.getFullYear();
        var month = time.getMonth() + 1;
        var date = time.getDate();
        $(h2).text(year + '/' + month + '/' + date);//TODO 放时间
        var h1 = document.createElement('h1');
        $(h1).text(data[i].title);

        $(header).append(h2);
        $(header).append(h1);

        $(listItem).append(img);
        $(listItem).append(header);

        $(self).append(listItem);
    });
};