Django ile geliştirilmiş sınav sistemidir.

Kullanıcıların giriş yaparak sadece çözmeleri için izin verilen soruları çözebileceği bir sistemdir. Kullanıcıların çözebileceği sorular grupları üzerinden yapılır. Gruplar tanımlanır ve her kullanıcı bu gruplara atanır. Daha sonra her grup için çözebileceği sınav tanımlamaları yapılır. Kullanıcılar da bu tanımlamalarda bulundukları gruplar için atana soruları çözebilirler. Grup ve sınav tanımlaması GroupExam modelinde yapılır.


Kullanıcı başladığı sınavı bitirmek zorundadır. Her sınav için kayıt yapılırken zaman ataması yapılır. Bu zaman içerisinde sınav bitirilmelidir. Sınav tanımlaması yapılırken sınavın başlama durumu girilir. Eğer sınav başladı ise kullanıcı sınavı görebilir ve çözebilir. Aksi taktirde çözemeyecektir.

Kullanıcılar sistemde daha önce çözdükleri görebilirler. My Exam menüsü altındadır. Daha önce çözdükleri soruyu görebilmeleri için sınav içerisinde görebilir seçeneğinin seçili olması gerekir. 

Kullanıcılar ve çözdükleri sınavlar UserExam modeli altında bulunur. Kullanıcıların çözdüğü her soru ise QuestionUserAnswer modeli altındadır. Kullanıcı sınavı bitirdikten sonra UserExam modeline eklenir. 