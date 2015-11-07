var db = {
    //数据值
    "oid":"",                    //news ID
    "title":"",                 //活动标题
    "title_img":"",             //正方形首图片
    "content_img":"",           //详情图
    "time":"",                  //时间
    "type":"",                  //类型
    "is_authorized":"",         //是否经过授权
    "authorized_remark":"",     //授权备注，default:null
    //检测值
    "view":""                   //浏览量
}

/*
******************************************
** 这里规定 ONEWS.DIVINITI.CN 的访问API **
******************************************

    /onews/         POST    新建一个ONEWS
    /onews/{id}     DELETE  删除一个ONEWS
    /onews/{id}     GET     获取一个ONEWS

    e.g. POST   http://onews.diviniti.cn/onews         发布ONEWS
    e.g. GET    http://onews.diviniti.cn/onews/150606  获取ID 为150606的ONES
    e.g. DELETE http://onews.diviniti.cn/onews/150606  删除ID 为150606的ONES
*/