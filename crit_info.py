# -*- coding: utf-8 -*-

crit_directory = {
                0:('Search English term',"SELECT * FROM dictionary WHERE Term LIKE '%<placeholder>%'"),
                1:('Search Chinese translation (may contain English text)',"SELECT * FROM dictionary WHERE Translation LIKE '%<placeholder>%'")
}