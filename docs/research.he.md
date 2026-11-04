# מדריכים ולקחים לבניית הפלטפורמה

המקורות נבדקו ב־5 באוקטובר 2026. מדריכי ביצוע נבחרו מהתיעוד של מפתחי הכלים; לקחים היסטוריים נבחרו מדוחות של הצוותים המעורבים ומניסיון מקצועי מפורש. המלצות המימוש והיעדים המספריים במסמכי הפרויקט הם הסקה שלנו, ואינם מדידה שהמקורות ביצעו עבור האפליקציה הזאת.

## לקחים שמחליפים סדר עבודה שגוי

| מקור ותאריך | מה מתועד | ההשלכה שאנחנו מסיקים לפרויקט |
| --- | --- | --- |
| [Sharetribe Strategy](https://www.sharetribe.com/academy/marketplace-strategy-principles/), פורסם 19.9.2025, עודכן 18.9.2026 | מייסדי marketplaces משקיעים לעיתים חודשים במערכת לפני בניית בסיס משתמשים; זמינות התאמות בין הצדדים מרכזית למוצר | נבחר קהילה קטנה, נגייס פרויקטים אמיתיים ונלווה חיבורים במקביל לפיתוח |
| [Martin Fowler, Monolith First](https://martinfowler.com/bliki/MonolithFirst.html), 3.6.2015 | מתוך תצפיותיו המקצועיות, גבולות שירותים קשה לקבוע בתחילת מוצר; פיצול מוסיף עלות | Spring יתחיל כיישום אחד עם מודולים; אין הבטחה שפירוק עתידי תמיד יהיה קל |
| [GitLab Database Postmortem](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/), אירוע 31.1.2017, דוח 10.2.2017 | מחיקה שגויה ונהלי גיבוי ושחזור שנכשלו האריכו התאוששות; לא הייתה בעלות ברורה על בדיקת השחזור | נגדיר סביבות נפרדות, אחריות וגיבוי שנוסה בשחזור לפני בטא |
| [Vercel Middleware Postmortem](https://vercel.com/blog/postmortem-on-next-js-middleware-bypass), 25.3.2025 | חולשת CVE-2025-29927 אפשרה עקיפת middleware במסלולי פריסה מסוימים; Vercel מזהירה מהגנה הנשענת עליו בלבד | כל endpoint של Spring וכל גישה למסמך פרטי יבדקו הרשאה גם כשהממשק הסתיר את הפעולה |

דוחות GitLab ו־Vercel הם אירועים מתועדים. מאמר Fowler הוא ניסיון ותצפיות מקצועיות, לא ניסוי מבוקר. Sharetribe היא ספקית מסחרית בתחום ולכן יש לה עניין עסקי; נשתמש בתובנות על שוק דו־צדדי, בלי להסיק מהן שאנחנו צריכים את המוצר שלה.

## מלכודות שהתיעוד העדכני מזהיר מפניהן

| מלכודת | מקור רשמי | מה נעשה בפועל |
| --- | --- | --- |
| session מפוענח נתפס כהוכחת זהות | [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/nextjs) | אימות claims בשרת ו־JWT ב־Spring; לא נסמוך על user מתוך getSession |
| cache משתף תשובה עם cookies או מידע פרטי | [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/nextjs), [Next.js Authentication](https://nextjs.org/docs/app/guides/authentication) | נפריד תצוגה ציבורית ממידע אישי ונבדוק שני משתמשים ברצף |
| טבלה מוגנת נתפסת כהגנה אוטומטית לערוץ Broadcast | [Realtime Authorization](https://supabase.com/docs/guides/realtime/authorization) | RLS לערוץ פרטי; בדיקה גם עם socket פתוח בזמן שינוי הרשאה |
| אירוע Realtime נתפס כהיסטוריית הודעות | [Database Changes](https://supabase.com/docs/guides/realtime/subscribing-to-database-changes) | היסטוריה במסד; השלמה לפי סמן לאחר ניתוק |
| כל connection string נחשב מתאים לכל ORM | [PostgreSQL Connections](https://supabase.com/docs/guides/database/connecting-to-postgres) | בדיקת pooler, SSL ו־JDBC, כולל prepared statements ותקציב חיבורים |
| threads ממשיכים לפעול אחרי HTTP response | [Cloud Run General Tips](https://docs.cloud.google.com/run/docs/tips/general) | outbox עם worker מופעל במפורש או Job; לא scheduling מקרי בתוך instance |
| דוא״ל Auth המובנה מתאים לכל משתמשי בטא | [Supabase SMTP](https://supabase.com/docs/guides/auth/auth-smtp) | custom SMTP, דומיין מאומת ובדיקת delivery לפני בטא |
| גיבוי מסד כולל קורות חיים ותמונות | [Supabase Backups](https://supabase.com/docs/guides/platform/backups) | גיבוי או שחזור נפרדים ל־Storage |
| ביטול הרשאה מבטל מיד URL חתום שכבר נשלח | [Private Downloads](https://supabase.com/docs/guides/storage/serving/downloads) | URLs קצרי חיים ובדיקת הרשאה בכל בקשה חדשה |

אלה אזהרות ותנאי הפעלה מהתיעוד, לא טענה שכל אחת מהן כבר גרמה לאירוע אצל משתמש בפרויקט שלנו.

## מסלול לימוד וביצוע לפי הסדר

| מתי | מדריך | מה ללמוד ממנו | התאמה לפרויקט שלנו |
| --- | --- | --- | --- |
| בסיס web | [Next.js Installation](https://nextjs.org/docs/app/getting-started/installation) | התקנה, App Router והפעלת פרויקט | לנעול גרסאות ולבנות מסך קטן עם RTL |
| בסיס API | [Spring REST Service](https://spring.io/guides/gs/rest-service/) | Controller, DTO ותגובה ב־JSON | לבנות endpoint אחד; לא להפוך דוגמת Greeting לארכיטקטורת מוצר |
| auth | [Supabase SSR](https://supabase.com/docs/guides/auth/server-side/nextjs), [Spring JWT](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html) | cookies, sessions, issuer, audience ו־JWKS | להוכיח אתר → token → Spring לפני בניית רוב ה־API |
| מסד מקומי | [Supabase CLI](https://supabase.com/docs/guides/local-development) | שירותים מקומיים עם Docker | לבדוק גם שירותים מנוהלים, מעבר למסד PostgreSQL רגיל |
| JDBC | [Connecting to Postgres](https://supabase.com/docs/guides/database/connecting-to-postgres) | שיטות חיבור ו־pooling | להעתיק את host האמיתי מה־Connect dialog; לא להמציא hostname |
| migrations | [Spring Database Initialization](https://docs.spring.io/spring-boot/how-to/data-initialization.html) | Flyway ותלות PostgreSQL | מקור אחד לשינוי סכמת המוצר |
| מודולים | [Spring Modulith Fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html) | API של מודול ותלות בין packages | מודולים לפי מוצר, לא services נפרדים |
| API משותף | [springdoc](https://springdoc.org/), [OpenAPI Generator](https://openapi-generator.tech/docs/generators/typescript-fetch/) | schema ויצירת לקוח TypeScript | API contract אחד ל־web ול־mobile |
| קבצים | [Storage Access Control](https://supabase.com/docs/guides/storage/security/access-control), [Downloads](https://supabase.com/docs/guides/storage/serving/downloads) | buckets פרטיים, policies וקישורים חתומים | CV קשור לפונה, גרסה והרשאה מסוימת |
| realtime | [Database Changes](https://supabase.com/docs/guides/realtime/subscribing-to-database-changes), [Authorization](https://supabase.com/docs/guides/realtime/authorization) | Broadcast, triggers וערוצים פרטיים | אירוע עדכון בלבד; השרת מוסר תוכן לפי הרשאה |
| דוא״ל ועבודה מתוזמנת | [Supabase SMTP](https://supabase.com/docs/guides/auth/auth-smtp), [Resend Java](https://resend.com/docs/send-with-java), [Cloud Run Jobs](https://docs.cloud.google.com/run/docs/execute/jobs-on-schedule) | delivery, API ותזמון עבודה | הפרדת הודעות Auth מדוא״ל מוצר עם outbox |
| בדיקות מסד | [Testcontainers Spring](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/) | מסד אמיתי בבדיקות integration | ללמוד את הדפוס ולבדוק גרסאות תלויות לפני העתקת pom |
| בדיקות UI | [Playwright Best Practices](https://playwright.dev/docs/best-practices) | בידוד בדיקות והמתנה להתנהגות | שני contexts למשתמשים ואדם שלישי לא מורשה |
| פריסה מוקדמת | [Java on Cloud Run](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-java-service), [Next.js Self Hosting](https://nextjs.org/docs/app/guides/self-hosting) | שרתים בקונטיינרים ותנאי hosting | אותו ארגון שירותים ב־staging וב־production |
| CI לענן | [Google Deployment Identity](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines) | אמון ב־GitHub OIDC | לצמצם צורך במפתחות Google ארוכי חיים |
| לפני בטא | [Supabase Production Checklist](https://supabase.com/docs/guides/deployment/going-into-prod), [Backups](https://supabase.com/docs/guides/platform/backups) | readiness ושחזור | לבצע עם הזהויות וההגדרות שלנו, לא רק לקרוא |
| מובייל בהמשך | [Expo Monorepos](https://docs.expo.dev/guides/monorepos/) | workspaces ותקלות dependency resolution | לבדוק התאמה ל־React של Expo, לא לשתף בכוח כל רכיב web |

## כיצד להשתמש במדריכים בלי להעתיק טעויות

נבדוק שהמדריך שייך לשכבה שבחרנו: Spring MVC ולא WebFlux כאשר אין צורך ב־reactive; Supabase Auth ולא מערכת סיסמאות מקומית שמופיעה בדוגמת Next.js אחרת. קוד מסד שמופיע במדריך Next.js ילמד אותנו rendering, אך בפרויקט שלנו השרת העסקי הוא Spring.

בעת העתקת דוגמה נבדוק version, deprecated APIs, שמות starters, מעברי Javax/Jakarta ותאימות ספריות. מדריך ישן יכול ללמד מושג תקף, אך פקודת התקנה שלו לא תהיה מקור לנעילת dependency. טבלאות Boot ו־springdoc שנבדקו הן נקודת ההתחלה; נבדוק שוב בעת ההקמה. [Spring Boot Requirements](https://docs.spring.io/spring-boot/system-requirements.html), [springdoc Compatibility](https://springdoc.org/)

נריץ בכל פעם דוגמה קטנה עם מקרה כשל אחד לפני שנשלב אותה בפרויקט. אחר כך נחבר לפרוסה מוצרית: משתמש, הרשאה, נתון ותוצאה. מספר כלי התשתית אינו מדד להתקדמות; אדם שהצליח להגיע מהתעניינות לשיתוף פעולה הוא המדד המרכזי.

## מחקר על הזדמנויות למעצבים ותיקי עבודות

נבדק ב־5 באוקטובר 2026 בעקבות שיחת הגדרת המוצר. המקורות להלן מצביעים על ערוצים קיימים; הם אינם נתוני שכיחות על החיפוש של מעצבים בישראל ואינם מוכיחים ביקוש לפלטפורמה שלנו. עדיין נדרשות שיחות עם משתתפים פוטנציאליים.

| מקור | מה נמצא | מה כדאי לבדוק במוצר |
| --- | --- | --- |
| [Open Source Design](https://opensourcedesign.net/resources/how-to-join/), [מדריך לפרסום תפקיד](https://opensourcedesign.net/jobs/writing-job-posts/) | לוח בקשות עיצוב בקוד פתוח, כולל התנדבות; המדריך מדגיש אחריות ברורה, שקיפות בתמורה וערך של עבודה עם מפתחים | להציג יכולת נדרשת, היקף, ליווי ותועלת למשתתף |
| [UX Rescue](https://www.uxrescue.org/) | חיבור לפרויקטים בהתנדבות דרך טופס וקהילת Slack; האתר מציין אישור של הארגונים להצגת הפרויקט בתיק עבודות | להגדיר מראש מה המשתתף יכול להציג |
| [Startup Designers](https://www.startupdesigners.co/), [ADPList](https://adplist.org/ai) | קהילה ומנטורינג בישראל, ומנטורינג בינלאומי הכולל ביקורת תיקי עבודות | אלה ערוצי קהילה ומשוב, ולא ראיה שהם מספקים פרויקטים חיים לכל משתתף |
| [Create Magazine על פרויקט בהתנדבות](https://www.createmagazine.co.il/כניסה-לתחום/פרויקט-בהתנדבות-איך-תשמרו-על-עצמכם/) | ניסיון של איש UX בישראל: חשיבות של גבולות זמן ותכולה, אחריות אישית והצגת העבודה; מוזכרים קשרים, מוסדות לימוד וארגוני התנדבות כערוצי חיפוש | להבהיר ציפיות לפני הצטרפות ולבדוק את החשש מעבודה שמתארכת |
| [NN/g על בניית תיק עבודות](https://www.nngroup.com/articles/ux-design-portfolios/) | תיק עבודות מתאר תפקיד אישי, בעיה, תהליך, תוצרים, תוצאה ולמידה | רשימת פרויקטים לבדה אינה מספקת את כל הראיות; עדיף תיאור תרומה עם תהליך ותוצאה |

הסקת מוצר מוצעת: ההזדמנות אינה רק למצוא פרויקט, אלא למצוא שיתוף פעולה עם היקף ברור ותרומה שניתן להציג. אין להסיק מהמחקר שכל בעל פרויקט יוכל לספק ליווי, או שכל משתתף יסכים לתרום ללא תשלום. המסקנות המשפטיות שבמקורות לא אומצו כמדיניות לפלטפורמה.

## דוגמאות לצרכים בפרויקטים טכנולוגיים

אלה דוגמאות לפרסומים של בעלי פרויקטים, לא מדגם מייצג ולא הוכחה שהחיבור או העבודה הצליחו:

- [OpenStrap](https://opensourcedesign.net/jobs/looking-for-designers-for-openstrap-an-open-source-fitness-app/) מבקש מערכת עיצוב וכמה מסכים מרכזיים לאפליקציית כושר, ומציע קרדיט ללא התחייבות לתשלום. התיאור מציין שימוש קודם ב־AI בעיצוב ומבקש עיצוב שמבוסס על מחקר. הדוגמה מדגישה גם צורך מקצועי וגם קושי של היקף ותמורה.
- [Corro](https://opensourcedesign.net/jobs/front-end-developer-ui-for-corro-an-accessibility-first-board-card-game-platform/) מחפש פיתוח ממשק בשיתוף מעצב, תוך שמירה על נגישות, במוצר משחקים שניתן להתנסות בו. התפקיד מגדיר יכולת נדרשת ושיפורים ממוקדים.
- [Code for Israel](https://codeforisrael.org/) מתאר צוותי התנדבות של מפתחים, מעצבים, אנשי מוצר ודאטה ומציג מוצרים שנבנו לצרכים חברתיים וציבוריים בישראל. זה מקור של הארגון עצמו, ולא הערכה חיצונית להיקף הפעילות או לנכונות של מתחילים להשתתף.

בדפי Open Source Design מופיעות גם אזהרות לגבי טריות הפרסומים שאינן תואמות את התאריכים המוצגים בחלק מהדפים. לכן אין לראות בהם אישור שהגיוס עדיין פתוח. ההסקה המוצרית שלנו היא לבדוק אחריות מקצועית מוגדרת בתוך פרויקט, להציג יכולת נדרשת, ליווי והיקף, ולבדוק ביקוש בפיילוט ישראלי.

## בדיקה ראשונית של השתתפות ללא תשלום בישראל

נבדק ב־5 באוקטובר 2026 בעקבות תנאי המשתמש ששילוב חברות יהיה חוקי. [חוק שכר מינימום באתר הביטוח הלאומי](https://www.btl.gov.il/Laws1/00_0021_000000.pdf), סעיף 12, קובע שהזכות לפי החוק אינה ניתנת להתניה או לוויתור. [כל זכות על קביעת יחסי עובד ומעסיק](https://www.kolzchut.org.il/he/קביעת_קיומם_של_יחסי_עובד-מעסיק) מסביר שהסיווג נקבע לפי מהות היחסים ולא רק לפי ההסכם. [כל זכות על התלמדות](https://www.kolzchut.org.il/he/תשלום_שכר_עבור_תקופת_התלמדות,_הכשרה,_השתלמות_או_הכנות_למשמרת) מפרט שגם תקופת ניסיון או הכשרה במסגרת עבודה חייבת בשכר, והעובד אינו יכול לוותר עליו.

המשמעות לתכנון: אין לאשר גיוס ללא שכר רק משום שנכתב ״שיתוף פעולה״ או משום שמציעים קרדיט וניסיון. אין כאן קביעה שכל שיתוף פעולה בהתנדבות אסור, או שכל פרויקט אישי/עמותה מותר. מדיניות סוגי הפרויקטים ותנאי הפעילות צריכה להיבחן מקצועית, במיוחד במקרים של השתלבות בעסק, ניהול שוטף, שעות קבועות או תפקיד המחליף עובד. יש לברר גם את חובות הפלטפורמה עצמה; המחקר הנוכחי אינו הכרעה לגביהן.

## פרופיל מקצועי וטופס השלמה

נבדק ב־5 באוקטובר 2026 לצורך בקשת המשתמש לסקור את הפרופיל הבסיסי. [NN/g — הפחתת העומס בטפסים](https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/), מ־18 ביולי 2025, ממליץ על ארגון שדות לפי נושא, הצגת מידע רלוונטי לפי שלב וסימון מפורש של חובה ובחירה. ההסקה המוצרית שלנו: להשלים בסיס מקצועי לפני פנייה או פרסום ולהשאיר הרחבות לבחירה; זו הצעה לבדיקה ולא אימות של שדות הפרופיל שלנו.

[GitHub — אודות הפרופיל](https://docs.github.com/en/account-and-profile/concepts/personal-profile) מתאר מידע אישי ומקצועי שהאדם בוחר לשתף, לצד פעילות ופריטים מוצמדים. ההבחנה במוצר שלנו היא שקישור לפרופיל מקצועי אינו חובה לפרסם את מאגר קוד הפרויקט. [תיעוד תרומות GitHub](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference) גם מבחין בין תצוגת כמות תרומות פרטיות לבין פרטי התרומות הנראים רק לבעלי גישה; אין צורך לדרוש שינוי נראות של מאגרים כחלק מדרישת הרקע.

## חסיון משוב וזיהוי בשיתוף פעולה של שני אנשים

נבדק ב־5 באוקטובר 2026 בעקבות רצון המשתמש להגן על זהות המדווח. [ICO על זיהוי מתוך הקשר והסקת מידע](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/how-do-we-ensure-anonymisation-is-effective/) מסביר שהסרת מזהים ישירים אינה מבטיחה שלא ניתן לקשר מידע לאדם, וכי ידע נוסף של מקבל המידע משפיע על הזיהוי. ההסקה המוצרית שלנו: בשיתוף פעולה של שני אנשים, טקסט או סיכום חוויה ללא שם, ולעיתים שינוי במוניטין, עשויים להסגיר את מקור הדיווח. משוב חסוי מול הצד השני צריך להיות מוגדר לפי מי שרואה אותו ולפי דרך השימוש בו; סיכום אוטומטי אינו הבטחת אנונימיות.

[Airbnb — ביקורות על אירוח](https://www.airbnb.com/help/article/13) מפרסם את הביקורות לאחר ששני הצדדים הגישו, או לאחר 14 ימים. זו דוגמה להשהיית חשיפה עד לאחר כתיבת המשוב, ולא הוכחה שהכותב אינו מזוהה או שהמנגנון יתאים למוצר שלנו. טרם נבחר מנגנון משוב או מוניטין; המלצתנו לבחון בנפרד את מטרת הדיווחים התקופתיים ואת משוב הסיום.

[Fradkin, Grewal ו־Holtz, ניסוי שדה במערכת המוניטין של Airbnb, 2021](https://pubsonline.informs.org/doi/abs/10.1287/mksc.2021.1311) מצא שהסתרת ביקורות עד להגשת שתיהן הגדילה את היקף המשוב והפחיתה תגובות של נקמה והדדיות בדירוג. השינויים במשוב לא תורגמו בניסוי להפחתת בחירה שלילית בשוק. הלקח לתכנון שלנו: עיצוב המשוב משנה את ההתנהגות; אין להניח שיותר דירוגים או הסתרת הכותב לבדם מייצרים התאמות טובות יותר. זה מחקר על אירוח, לא אימות של מערכת המוניטין שלנו, והמחקר עצמו אינו מדריך חדש מ־2026.

## דירוג קצר ושאלות לפי תפקיד

נבדק ב־5 באוקטובר 2026 בעקבות בחירת המשתמש בדירוגי 1–5 וסעיפים שונים לכל צד. [NN/g על סולמות דירוג](https://www.nngroup.com/articles/rating-scales/), נבדק מחדש ב־7 באוגוסט 2026, ממליץ על תוויות מובנות, טקסט לבחירה ואפשרות ״לא רלוונטי״. ההסקה שלנו היא שסעיף שאינו רלוונטי לא צריך להפוך לציון אפס, ושיש להגדיר משמעות אחידה לנקודות הסולם.

[Pew Research Center על הימנעות ממענה לשאלות פתוחות](https://www.pewresearch.org/decoded/2021/10/14/why-do-some-open-ended-survey-questions-result-in-higher-item-nonresponse-rates-than-others/), 2021, מציג הבדלים בהיקף המענה בין שאלות סגורות ופתוחות ובין רמות מאמץ שונות. זה תומך בכיוון של תשובות קצרות וטקסט לבחירה, אך אינו מוכיח שסולם 1–5 או שלוש השאלות שלנו הם הפתרון המתאים לקהל הזה. הכמות, המדדים והנוסחה לציון ציבורי עדיין דורשים אפיון ובדיקת משתמשים.

## נושאים נוספים במשוב הסיום

נבדק ב־9 באוקטובר 2026. [CATME על חמשת ממדי עבודת הצוות](https://info.catme.org/features/catme-five-dimensions/) כולל התנהלות מכבדת ושימוש במשוב בהערכת אינטראקציה בין חברי צוות. [מחקר התיקוף של URSSA מ־2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4710391/) מבחין בין דיווח על התקדמות אישית לבין שביעות רצון מהמנחים ומההתנסות; [אוניברסיטת קולורדו](https://www.colorado.edu/eer/research-areas/undergraduate-research/evaluation-tools-undergraduate-research-student-self) מציגה את הכלי להערכת תוצאות התנסות במחקר מדעי לתואר ראשון.

למוצר מוצעות שאלות סיום על יחס מכבד ועל עבודה עם משוב, ועוד שאלה חסויה על התקדמות לעבר מטרת ההצטרפות. דירוג היחסים יתייחס לתפקיד ולציפיות שסוכמו; התקדמות אישית תיאסף בנפרד ולא תיכנס לציון המוניטין. הכלים והמחקר מגיעים ממסגרות לימודיות, והשאלות והציון המוצעים כאן דורשים בדיקה עם בעלי פרויקטים ומשתתפים בפלטפורמה. אין מספר שאלות מומלץ אוניברסלי או סף פרסום שניתן להסיק ממקורות אלה.

## השתתפות בפרויקט בקורות חיים ותנאי סודיות

נבדק ב־9 באוקטובר 2026. [Yale על קורות חיים טכניים](https://ocs.yale.edu/resources/stemconnect-technical-resume-sample/) כולל ניסיון בתשלום וללא תשלום, פרויקטים עצמאיים והתנדבות, וממליץ לתאר את התרומה והיכולות הרלוונטיות. [Berkeley על דוגמאות לקורות חיים](https://www.career.berkeley.edu/prepare-for-success/resumes/sample-resumes/) מציע להציג פרויקטים במסגרת פרויקטים או ניסיון ולתאר את התפקיד והתוצאות האישיות. זו תמיכה מקצועית באפשרות להציג ניסיון בפרויקט, ולא הבטחה להכרה בו כוותק, להסמכה או לקבלה לעבודה בישראל.

סיכום השתתפות ותיאור תרומה אינם אישור גורף לחשיפת תוצרים או מידע פנימי. לדוגמה, [מסמכי מכרז משרד האוצר 1/2019](https://mr.gov.il/ilgstorefront/he/p/attachment/005056BF4DAB1EDA969D84A5175C211B/%D7%9E%D7%A1%D7%9E%D7%9B%D7%99%20%D7%94%D7%9C%D7%99%D7%9A), סעיף 10 בעמוד 6, דורשים אישור מראש ובכתב להעברת ממצאים ונתונים ולהצגת תוצאות עבודה. זה הסכם מסוים לשירותים רפואיים, ולא כלל החל אוטומטית על שיתוף הפעולה במוצר שלנו.

המשמעות למוצר: אפשר להגביל הצגת תוצרים ועדיין להסכים על אזכור עובדתי בקורות חיים. כדי לעמוד בתנאי המשתמש, מוצע להסדיר מראש אזכור של שם הפרויקט הציבורי, תפקיד, תקופה ותיאור תרומה מאושר, ולבסס אותו על רשומת התרומה לאחר סיום. נוסח ההרשאה והתאמתו להסכמי סודיות ולזכויות אחרים ייבדקו משפטית לפני ההשקה; מדריך קריירה אינו קובע היתר משפטי לפרויקט מסוים.

## גבולות המחקר

המחקר הזה בוחן ארכיטקטורה, דרך ביצוע ולקחים תפעוליים. הוא אינו אימות חדש של כל המתחרים ומשרות העבודה שנזכרו בשיחה, ואינו קביעה משפטית לגבי יחסי עבודה, תיווך או זכויות בתוצרים. לא הורצה כאן אפליקציה, לא נוצרו שירותי ענן ולא נמדדו latency ועלות של deployment שלנו. הפרטים האלה ייבדקו בשלבי העבודה שהוגדרו.

מחירים וזמינות מכסות משתנים. את העלות הסופית נחשב מתוך [Supabase Pricing](https://supabase.com/pricing), [Resend Pricing](https://resend.com/pricing) ו־[Cloud Run Pricing](https://cloud.google.com/run/pricing), לפי מספר הסביבות והשימוש בפועל.

## הגשת מועמדות קצרה בהשראת LinkedIn

נבדק ב־9 באוקטובר 2026. [מדריך LinkedIn להגשת מועמדות](https://www.linkedin.com/help/linkedin/answer/a512388/apply-for-jobs-on-linkedin?lang=en) מתאר פתיחת פרטי משרה, כפתור Easy Apply בראש העמוד, מילוי פרטים בחלון, בדיקה ושליחה. [המדריך להגשה ישירה](https://www.linkedin.com/help/linkedin/answer/a512348/) מתאר אפשרות לשמירת קורות חיים ותשובות לשימוש חוזר. [המדריך לשאלות במודעת Recruiter](https://www.linkedin.com/help/linkedin/answer/a413520/add-screening-questions-to-your-recruiter-job-post?lang=en) מציג שאלות לפי ניסיון וכלים, עם אפשרות לבחירה מתוך קטגוריות או ניסוח מותאם; תנאי הזמינות של היכולת מתייחסים למוצר Recruiter ולא לכל מודעה ב־LinkedIn.

ההתאמה למוצר שלנו כוללת כפתור בעמוד הפרויקט, בחירת תפקיד פתוח בתוך הטופס ושאלות שבעל הפרויקט מנסח בעצמו לפי התפקיד, בהתאם לבחירת המשתמש. המשתמש אישר עד שתי שאלות נוספות עם תשובה קצרה בטקסט, והוספתן לבחירת בעל הפרויקט. השימוש בפרופיל וברקע מקצועי שמורים ובחירה מראש כשיש תפקיד יחיד מתאים נשארים המלצות מוצר לבדיקה עם משתמשים. LinkedIn אינו מקור לבחירת תפקיד בתוך פרויקט בעל כמה תפקידים או לקביעת מגבלת השאלות שלנו; אלה החלטות והתאמות למבנה המוצר שלנו. אין להסיק מהמדריכים שיעור השלמה, התאמה של כל מי שנכנס לעמוד או מספר שאלות מיטבי לקהל שלנו. מדובר בהשראה למסלול, ללא החלטה על חיבור טכני ל־LinkedIn.
