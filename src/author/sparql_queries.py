search_query = """

SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q5;
    ?label "QUERY"@en.
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P106 ?statement1.
      ?statement1 (ps:P106/(wdt:P279*)) wd:Q36180.
    }
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 10

"""

author_details_query = """

SELECT DISTINCT 

    ?item ?itemLabel

    ?birthFullName ?birthFullNameLabel 
    ?birthFullNameInNativeLanguage ?birthFullNameInNativeLanguageLabel 
    ?causeOfDeath ?causeOfDeathLabel 
    ?countryOfCitizenship ?countryOfCitizenshipLabel 
    ?dateOfBirth ?dateOfBirthLabel 
    ?dateOfDeath ?dateOfDeathLabel 
    ?educatedAt ?educatedAtLabel 
    ?gender ?genderLabel 
    ?genre ?genreLabel
    ?lastWords ?lastWordsLabel 
    ?lifestyle ?lifestyleLabel 
    ?literaryMovement ?literaryMovementLabel 
    ?mannerOfDeath ?mannerOfDeathLabel 
    ?nativeLanguage ?nativeLanguageLabel 
    ?notableWorks ?notableWorksLabel 
    ?occupation ?occupationLabel 
    ?placeOfBirth ?placeOfBirthLabel 
    ?placeOfBurial ?placeOfBurialLabel 
    ?placeOfDeath ?placeOfDeathLabel 
    ?religion ?religionLabel 
    ?workPeriodStart ?workPeriodStartLabel 
    ?writingLanguage ?writingLanguageLabel 

    WHERE {

    VALUES ?item {

    wd:QUERY

  }

    OPTIONAL { ?item wdt:P1477 ?birthFullName. }
    OPTIONAL { ?item wdt:P1559 ?birthFullNameInNativeLanguage. }
    OPTIONAL { ?item wdt:P509 ?causeOfDeath. }
    OPTIONAL { ?item wdt:P27 ?countryOfCitizenship. }
    OPTIONAL { ?item wdt:P569 ?dateOfBirth. }
    OPTIONAL { ?item wdt:P570 ?dateOfDeath. }
    OPTIONAL { ?item wdt:P69 ?educatedAt. }
    OPTIONAL { ?item wdt:P21 ?gender. }
    OPTIONAL { ?item wdt:P136 ?genre. }
    OPTIONAL { ?item wdt:P3909 ?lastWords. }
    OPTIONAL { ?item wdt:P1576 ?lifestyle. }
    OPTIONAL { ?item wdt:P135 ?literaryMovement. }
    OPTIONAL { ?item wdt:P1196 ?mannerOfDeath. }
    OPTIONAL { ?item wdt:P103 ?nativeLanguage. }
    OPTIONAL { ?item wdt:P800 ?notableWorks. }
    OPTIONAL { ?item wdt:P106 ?occupation. }
    OPTIONAL { ?item wdt:P19 ?placeOfBirth. }
    OPTIONAL { ?item wdt:P119 ?placeOfBurial. }
    OPTIONAL { ?item wdt:P20 ?placeOfDeath. }
    OPTIONAL { ?item wdt:P140 ?religion. }
    OPTIONAL { ?item wdt:P2031 ?workPeriodStart. }
    OPTIONAL { ?item wdt:P6886 ?writingLanguage. }

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

"""
