CREATE TABLE foursquare (
      fsq_place_id        text,
      fsq_name            text,
      fsq_latitude        text,
      fsq_longitude       text,
      fsq_address         text,
      fsq_locality        text,
      fsq_region          text,
      fsq_postcode        text,
      fsq_admin_region    text,
      fsq_post_town       text,
      fsq_po_box          text,
      fsq_country         text,
      fsq_date_created    text,
      fsq_date_refreshed  text,
      fsq_date_closed     text,
      fsq_tel             text,
      fsq_website         text,
      fsq_email           text,
      fsq_facebook_id     text,
      fsq_instagram       text,
      fsq_twitter         text,
      fsq_category_ids    text,
      fsq_category_labels text,
      fsq_placemaker_url  text,
      fsq_unresolved_flags text,
      fsq_bbox            text
);

\copy foursquare FROM 'foursquare_clean.csv' WITH ( FORMAT csv, HEADER, DELIMITER ',', QUOTE '"', ESCAPE '"', NULL '')

