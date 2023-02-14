echo '------- determine QUADS version -------------'
docker exec quads bin/quads-cli --version

echo '------- define 3 clouds ---------------------'
echo 'exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01 --cloud-owner quads'
docker exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01 --cloud-owner quads
echo 'exec quads bin/quads-cli --define-cloud --cloud cloud02 --description cloud02 --cloud-owner quads'
docker exec quads bin/quads-cli --define-cloud --cloud cloud02 --description cloud02 --cloud-owner quads
echo 'exec quads bin/quads-cli --define-cloud --cloud cloud03 --description cloud03 --cloud-owner quads --cc-users "cc1 cc2"'
docker exec quads bin/quads-cli --define-cloud --cloud cloud03 --description cloud03 --cloud-owner quads --cc-users "cc1 cc2"

echo '------- redefine cloud01 w/o force ----------'
echo 'exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01'
docker exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01
echo '------- redefine cloud01 w/force ------------'
echo 'exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01 --force'
docker exec quads bin/quads-cli --define-cloud --cloud cloud01 --description cloud01 --force

echo '------- define hosts ------------------------'
echo 'exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor'
docker exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor
echo 'exec quads bin/quads-cli --define-host --host host02.example.com --default-cloud cloud01 --host-type vendor'
docker exec quads bin/quads-cli --define-host --host host02.example.com --default-cloud cloud01 --host-type vendor

echo '------- redefine host01 w/o force ----------'
echo 'exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor'
docker exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor
echo '------- redefine host01 w/force ------------'
echo 'exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor --force'
docker exec quads bin/quads-cli --define-host --host host01.example.com --default-cloud cloud01 --host-type vendor --force


echo '------- list owners -------------------------'
echo 'exec quads bin/quads-cli --ls-owner'
docker exec quads bin/quads-cli --ls-owner
echo '------- list tickets ------------------------'
echo 'exec quads bin/quads-cli --ls-ticket'
docker exec quads bin/quads-cli --ls-ticket
echo '------- list qinq ---------------------------'
echo 'exec quads bin/quads-cli --ls-qinq'
docker exec quads bin/quads-cli --ls-qinq
echo '------- list wipe ---------------------------'
echo 'exec quads bin/quads-cli --ls-wipe'
docker exec quads bin/quads-cli --ls-wipe
echo '------- list ccusers ------------------------'
echo 'exec quads bin/quads-cli --ls-cc-user'
docker exec quads bin/quads-cli --ls-cc-user


echo '------- Add schedules'
echo 'exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2018-04-27 08:00" --schedule-end "2018-08-19 08:00" --schedule-cloud cloud01'
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2018-04-27 08:00" --schedule-end "2018-08-19 08:00" --schedule-cloud cloud01
echo 'exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2019-04-27 08:00" --schedule-end "2019-08-19 08:00" --schedule-cloud cloud02'
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2019-04-27 08:00" --schedule-end "2019-08-19 08:00" --schedule-cloud cloud02
echo 'exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2016-04-27 08:00" --schedule-end "2016-08-19 08:00" --schedule-cloud cloud03'
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2016-04-27 08:00" --schedule-end "2016-08-19 08:00" --schedule-cloud cloud03

echo '------- List schedules'
echo 'exec quads bin/quads-cli --ls-schedule --host host01.example.com'
docker exec quads bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
echo 'exec quads bin/quads-cli --rm-schedule --schedule-id 1 --host host01.example.com'
docker exec quads bin/quads-cli --rm-schedule --schedule-id 1 --host host01.example.com

echo '------- List schedules'
echo 'exec quads bin/quads-cli --ls-schedule --host host01.example.com'
docker exec quads bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
echo 'exec quads bin/quads-cli --rm-schedule --schedule-id 2 --host host01.example.com'
docker exec quads bin/quads-cli --rm-schedule --schedule-id 2 --host host01.example.com
echo 'exec quads bin/quads-cli --rm-schedule --schedule-id 3 --host host01.example.com'
docker exec quads bin/quads-cli --rm-schedule --schedule-id 3 --host host01.example.com

echo '------- Add interfaces'
echo 'exec quads bin/quads-cli --add-interface --interface-name em1 --interface-mac 00:00:00:00:00:00  --interface-switch-ip 10.12.67.247 --interface-port xe-0/0/0 --host host01.example.com'
docker exec quads bin/quads-cli --add-interface --interface-name em1 --interface-mac 00:00:00:00:00:00  --interface-switch-ip 10.12.67.247 --interface-port xe-0/0/0 --host host01.example.com

echo '------- List interfaces'
echo 'exec quads bin/quads-cli --ls-interface --host host01.example.com'
docker exec quads bin/quads-cli --ls-interface --host host01.example.com

echo '------- delete interfaces'
echo 'exec quads bin/quads-cli --rm-interface --interface-name em1 --host host01.example.com'
docker exec quads bin/quads-cli --rm-interface --interface-name em1 --host host01.example.com

echo '------- remove hosts and clouds -------------'
echo 'exec quads bin/quads-cli --rm-host --host host01.example.com'
docker exec quads bin/quads-cli --rm-host --host host01.example.com
echo 'exec quads bin/quads-cli --rm-host --host host02.example.com'
docker exec quads bin/quads-cli --rm-host --host host02.example.com
echo 'exec quads bin/quads-cli --rm-cloud --cloud cloud01'
docker exec quads bin/quads-cli --rm-cloud --cloud cloud01
echo 'exec quads bin/quads-cli --rm-cloud --cloud cloud02'
docker exec quads bin/quads-cli --rm-cloud --cloud cloud02
echo 'exec quads bin/quads-cli --rm-cloud --cloud cloud03'
docker exec quads bin/quads-cli --rm-cloud --cloud cloud03

echo '------- remove bogus hosts and clouds -------'
echo 'exec quads bin/quads-cli --rm-host --host bogus_host'
docker exec quads bin/quads-cli --rm-host --host bogus_host
echo 'exec quads bin/quads-cli --rm-cloud --cloud bogus_cloud'
docker exec quads bin/quads-cli --rm-cloud --cloud bogus_cloud
