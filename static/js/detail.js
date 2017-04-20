$(function () {
    $(".add").click(function () {
        var t = $(this).parent().find('input[class*="num_show"]');
        t.val(parseInt(t.val())+1);
        $('.num_show').trigger("change");
        setTotal();
    });

    $(".minus").click(function () {
        $(".num_show").trigger("change");
        var t = $(this).parent().find('input[class*="num_show"]');
        t.val(parseInt(t.val())-1);
        if ((parseInt(t.val()) - 1) < 1){
            t.val(1);
        }
        setTotal();
        $(".num_show").trigger("change");
    });

    function setTotal() {
        var s = 0;
        s = (parseInt($(".num_show").val())*parseInt($(".show_price > em").html())).toFixed(2);
        $(".total").children(":first").html(s);
    }

    $('.num_show').change(function () {
        $('.buy_btn').attr({href:$('.buy_btn').attr("href").split("?")[0] + '?id' + $('.add_card').attr('value')
        + "&&count=" + $(".num_show").val()});
    });

    $("#add_cart").click(function () {
        //加入购物车
    });

    $(".num_show").trigger("change");
});
