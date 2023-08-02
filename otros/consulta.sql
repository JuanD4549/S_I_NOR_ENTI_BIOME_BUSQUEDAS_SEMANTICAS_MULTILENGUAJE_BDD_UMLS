/*CREATE EXTENSION vector
*/
/*ALTER TABLE umls.mrconso ADD COLUMN embedding vector(3)*/
SELECT * FROM umls.mrconso WHERE str='1,2-dipalmitoylphosphatidylcholine'
SELECT * FROM umls.mrsty WHERE tui='T047'
-- FUNCTION: public.get_ngrams(text)

-- DROP FUNCTION IF EXISTS public.get_ngrams(text);

CREATE OR REPLACE FUNCTION umls.get_ngrams(
	sent text)
    RETURNS TABLE(ngram_t text, count bigint, lenght integer) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$

BEGIN
return query
		with my_table(sentence) as (
    values (sent)
    ),

words as (
    select id, word
    from my_table,
    regexp_split_to_table(lower(sentence), '[^a-zA-Záéíóú]+') with ordinality as t(word, id)
    where word <> ''
    )

select ngram, count(*), length
from (
    select distinct on(id, ngram) id, ngram, length
    from (
        select id, word as ngram, 1 as length
        from words
        union all   
        select id, concat_ws(' ', word, lead(word, 1) over w), 2
        from words
        window w as (order by id)
        union all
        select id, concat_ws(' ', word, lead(word, 1) over w, lead(word, 2) over w), 3
        from words
        window w as (order by id)
		union all
        select id, concat_ws(' ', word, lead(word, 1) over w, lead(word, 2) over w, lead(word, 3) over w), 4
        from words
        window w as (order by id)
        ) s
    order by id, ngram, length
    ) s
group by ngram, length
order by length, min(id);
END;
$BODY$;
