# URLS CON EMOJIS Y CARACTERES ESPECIALES

Según lo que investigue en el siguiente link: [¿Como funcionan los emojis en los dominios de las url?](https://es.wikipedia.org/wiki/Dominio_emoji)

Los carácteres especiales y los emojis vienen codeados en **Punycode** por ende la forma en la que deberíamos hacerlo funcionar
en este laboratorio sería mediante una normalización a esta codificación, esto lo hacemos mediante la librería **unicodedata** la
cual viene con una función _normalize_ la cual nos ayudará a decodificar un emoji o caracter especial (en caso de no ser ninguno
de estos simplemente lo deja como está ya que no es necesario normalizar nada).