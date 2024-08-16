-- You can execute this as-is, in your schema. Pay special
-- attention to the Movie_ID Primary Key. This is what 
-- allows you to take advantage of ORDS Route Parameters.
-- 
CREATE TABLE "MOVIE" (
    "MOVIE_ID"     NUMBER,
    "TITLE"        VARCHAR2(200 BYTE),
    "BUDGET"       NUMBER,
    "GROSS"        NUMBER,
    "LIST_PRICE"   NUMBER,
    "GENRES"       JSON,
    "SKU"          VARCHAR2(30 BYTE),
    "YEAR"         NUMBER,
    "OPENING_DATE" DATE,
    "VIEWS"        NUMBER,
    "CAST"         JSON,
    "CREW"         JSON,
    "STUDIO"       JSON,
    "MAIN_SUBJECT" VARCHAR2(500 BYTE),
    "AWARDS"       JSON,
    "NOMINATIONS"  JSON,
    "RUNTIME"      NUMBER,
    "SUMMARY"      CLOB
)
NO INMEMORY;

CREATE UNIQUE INDEX "PK_MOVIE_ID" ON
    "MOVIE" (
        "MOVIE_ID"
    );

ALTER TABLE "MOVIE"
    ADD CONSTRAINT "PK_MOVIE_ID" PRIMARY KEY ("MOVIE_ID")
        USING INDEX "PK_MOVIE_ID" ENABLE;