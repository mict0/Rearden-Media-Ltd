def parse_campaign_name(campaign_name: str) -> dict:
    parsed_campaign_name = {}
    parsed_campaign_name["product_name"] = _get_product_name(campaign_name)
    parsed_campaign_name["category_name"] = _get_category_name(campaign_name)
    parsed_campaign_name["avatar_id"] = _get_avatar_id(campaign_name)
    parsed_campaign_name["geo"] = _get_geo(campaign_name)
    parsed_campaign_name["link"] = _get_link(campaign_name)
    parsed_campaign_name["cold"] = _get_cold(campaign_name)
    return parsed_campaign_name


def _get_product_name(name: str, keyword: str = "P_") -> str:
    return _find_keyword(name, keyword)


def _get_category_name(name: str, keyword: str = "C_") -> str:
    return _find_keyword(name, keyword)


def _get_avatar_id(name: str, keyword: str = "_AV_") -> str:
    return _find_keyword(name, keyword)


def _get_geo(name: str, keyword: str = "_C_") -> str:
    return _find_keyword(name, keyword)


def _get_link(name: str, keyword: str = "_LD_") -> str:
    return _find_keyword(name, keyword)


def _get_cold(name: str) -> bool:
    return "cold" in name


def _find_keyword(name: str, keyword: str) -> str:
    if keyword in name:
        try:
            split = name.split(keyword)[1]
            value = split.split("_")[0]
            return value
        except Exception as e:
            print(f"Could not find {keyword} in name: {e}")
    return ""
