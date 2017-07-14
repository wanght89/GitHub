def parse_detail(self, response):
    article_item = ArticlespiderItem()
    # 通过css选择器提取字段
    front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
    title = response.css(".entry-header h1::text").extract()[0]
    create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace(".", "").strip()
    praise_nums = response.css(".vote-post-up h10::text").extract()[0]
    fav_nums = response.css(".bookmark-btn::text").extract()[0]
    match_re = re.match(".*?(\d+).*", fav_nums)
    if match_re:
        fav_nums = int(match_re.group(1))
    else:
        fav_nums = 0
    comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
    match_re = re.match(".*?(\d+).*", comment_nums)
    if match_re:
        comment_nums = int(match_re.group(1))
    else:
        comment_nums = 0
    content = response.css("div.entry").extract()[0]
    tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
    tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
    tags = ",".join(tag_list)

    article_item["url_object_id"] = get_md5(response.url)
    article_item["title"] = title
    article_item["url"] -= response.url
    try:
        create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    article_item["create_date"] = create_date
    article_item["front_image_url"] = front_image_url
    article_item["prasie_nums"] = praise_nums
    article_item["comment_nums"] = comment_nums
    article_item["fav_nums"] = fav_nums
    article_item["tags"] = tags
    article_item["content"] = content
    yield article_item