
def get_dtype_from_similarity(similarity_col):
    return {
        "fsq_place_id": "string",
        "fsq_name": "string",
        "fsq_latitude": "float64",
        "fsq_longitude": "float64",
        "fsq_address": "string",
        "fsq_locality": "string",
        "fsq_region": "string",
        "fsq_postcode": "string",
        "fsq_admin_region": "string",
        "fsq_post_town": "string",
        "fsq_po_box": "string",
        "fsq_country": "string",
        "fsq_date_created": "string",
        "fsq_date_refreshed": "string",
        "fsq_date_closed": "string",
        "fsq_tel": "string",
        "fsq_website": "string",
        "fsq_email": "string",
        "fsq_facebook_id": "string",
        "fsq_instagram": "string",
        "fsq_twitter": "string",
        "fsq_category_ids": "string",
        "fsq_category_labels": "string",
        "fsq_placemaker_url": "string",
        "fsq_unresolved_flags": "string",
        "fsq_bbox": "string",
        "fsq_geom": "string",
        "osm_id": "string",
        "osm_class": "string",
        "osm_type": "string",
        "osm_name": "string",
        "osm_address": "string",
        "osm_extratags": "string",
        "osm_geometry": "string",
        "osm_latitude": "float64",
        "osm_longitude": "float64",
        "osm_geom": "string",
        similarity_col: "float64",
        "fsq_osm_distance" : "float64",
    }

def get_dtype(similarity_col=None, which=None):
    if similarity_col is not None:
        return get_dtype_from_similarity(similarity_col)
    elif which == 'lev':
        return get_dtype_from_similarity("fsq_osm_name_similarity_score_lev")
    elif which == 'trg':
        return get_dtype_from_similarity("fsq_osm_name_similarity_score_trg")
    else:
        raise ValueError(f"Unknown which value: {which}. Expected 'lev' or 'trg'.")