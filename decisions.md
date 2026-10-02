# Tasarım kararları

## Alan motorunu CLI'dan ayırmak

`run(config)` orkestrasyonu kaynak kodun doğrudan test edilebilmesini sağlar. JSON arayüz taşınabilirliği artırır; bu sürüm kullanıcı arayüzü barındırmaz.

## Seçilen yöntem

Kısmi tahsis, çoklu referans, kuruş bazlı korunum. Tutarlar tamsayı minor unit; açık referans yoksa yalnız bir uygun aday otomatik eşleşir.

## Bilinçli sınır

Kur dönüşümü ve banka entegrasyonu yoktur; toleransla kapanan bakiyeler raporda görünmeye devam eder.

## Önerilen sonraki doğrulama

Gerçek kullanım hacmiyle testten önce mevcut kabul ve ret örneklerinin alan uzmanı tarafından onaylanması gerekir. Sonraki sürüm performans ölçümleri, dış adaptör sözleşmesi ve üretim gözlemlenebilirliğini ayrı karar kayıtlarında ele almalıdır.
