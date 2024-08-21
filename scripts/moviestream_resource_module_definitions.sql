
BEGIN
  ORDS.DEFINE_MODULE(
      p_module_name    => 'moviestream',
      p_base_path      => '/mymovies/',
      p_items_per_page => 25,
      p_status         => 'PUBLISHED',
      p_comments       => NULL);

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-genre',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-genre',
      p_method         => 'GET',
      p_source_type    => 'json/collection',
      p_items_per_page => 25,
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'select distinct genre
from movie, 
json_table(genres, ''$[*]'' columns(genre path ''$''))
order by 1 asc');

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-all',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-all',
      p_method         => 'GET',
      p_source_type    => 'json/collection',
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'SELECT movie_id, title, genres, year, substr(SUMMARY, 0,50) abbreviated_summary, runtime
FROM
    MOVIE
where json_exists(genres, ''$[*]?(@ == $v1)''
                    PASSING :genre as "v1")
    AND RUNTIME <= :runtime
    order by RUNTIME DESC');

  ORDS.DEFINE_PARAMETER(
      p_module_name        => 'moviestream',
      p_pattern            => 'movie-all',
      p_method             => 'GET',
      p_name               => 'genre',
      p_bind_variable_name => 'genre',
      p_source_type        => 'URI',
      p_param_type         => 'STRING',
      p_access_method      => 'IN',
      p_comments           => NULL);

  ORDS.DEFINE_PARAMETER(
      p_module_name        => 'moviestream',
      p_pattern            => 'movie-all',
      p_method             => 'GET',
      p_name               => 'runtime',
      p_bind_variable_name => 'runtime',
      p_source_type        => 'URI',
      p_param_type         => 'INT',
      p_access_method      => 'IN',
      p_comments           => NULL);

  ORDS.DEFINE_TEMPLATE(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-single/:id',
      p_priority       => 0,
      p_etag_type      => 'HASH',
      p_etag_query     => NULL,
      p_comments       => NULL);

  ORDS.DEFINE_HANDLER(
      p_module_name    => 'moviestream',
      p_pattern        => 'movie-single/:id',
      p_method         => 'GET',
      p_source_type    => 'json/item',
      p_mimes_allowed  => NULL,
      p_comments       => NULL,
      p_source         => 
'select summary, title, awards, gross from movie where movie_id =:id');

    
        
COMMIT;

END;
