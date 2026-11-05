# סביבות והרצה

מחקר מ־4 בנובמבר 2026. ב־4.11.2026 המשתמש אישר את התוכנית שהוצגה, ולכן **הכיוון** מסומן `אושר`: Kubernetes ללמידה, שלוש סביבות, Oracle OKE עם תוכנית יציאה, וניהול ב־GitOps. **בחירת הכלים הספציפיים מסומנת `מוצע`** וננעלת בשלב ההקמה. מחירים ומכסות נבדקו בנובמבר 2026; צריך לאמת אותם בדף הספק לפני הקמה.

## עקרונות
- **Supabase נשאר מנוהל, מחוץ לאשכול**: מסד הנתונים, Auth, Storage ו־Realtime. לא נריץ PostgreSQL בתוך האשכול ב־production, כי גיבוי, שחזור ו־upgrade של מסד stateful הם עבודה תפעולית שלא קשורה למוצר.
- **באשכול רצים** `web` (Next.js), `api` (Spring), ועבודות רקע כ־`CronJob`: outbox, תזכורות והסלמה למנהל אחרי שבוע.
- **הכול נייד בין ספקים.** התשתית מוגדרת כקוד, ולא משתמשים בשירות שקיים רק אצל ספק אחד מעבר ל־Load Balancer.
- **Git הוא מקור האמת** למה שרץ בכל סביבה (GitOps).

## כמה סביבות — `אושר`: שלוש, בשני שלבים
| סביבה | מתי נדרשת | איפה רצה | Supabase | מטרה |
| --- | --- | --- | --- | --- |
| **local** | מתחילת הקוד | k3d על Docker | Supabase CLI מקומי | פיתוח, למידת K8s וניסויים בלי עלות |
| **staging** | משלב 3 (הוכחת חיבורים) | אשכול בענן, namespace `staging` | פרויקט Free (נעצר אחרי 7 ימים בלי פעילות) | בדיקת OAuth, SMTP, SSL, ARM ופריסה אמיתית |
| **production** | בפתיחת הבטא | namespace `prod`, ובהמשך אשכול נפרד | פרויקט Pro (כ־$25 לחודש) | משתמשים אמיתיים |

- **אשכול אחד עם namespaces** עד הבטא. לכל namespace יוגדרו ResourceQuota ו־LimitRange, כדי ש־staging לא ירעיב את prod. כשיהיו משתמשים אמיתיים, production עובר לאשכול נפרד. [namespaces מול אשכולות](https://acquaintsoft.com/blog/multi-environment-kubernetes-setup-devops)
- **לא בשלב הזה: סביבת preview לכל PR.** Supabase Branching זמין רק בתוכניות בתשלום (כ־$0.013 לשעה לכל ענף), ולמפתח יחיד אין לזה ערך. נשקול כשיצטרף אדם נוסף. [Supabase Branching](https://supabase.com/docs/guides/platform/manage-your-usage/branching)
- k3d מהיר וקל יותר מ־kind ו־minikube לעבודה יומיומית; kind נשאר אפשרות לבדיקות CI. [השוואה](https://devopsboys.com/blog/kind-vs-k3d-vs-minikube-local-kubernetes-2026)

## איפה ירוץ האשכול — `אושר`: Oracle OKE, עם תוכנית יציאה
| אפשרות | עלות בפועל | שורה תחתונה |
| --- | --- | --- |
| **Oracle OKE Basic + Always Free A1** | $0: control plane חינם; 2 OCPU ו־12GB ARM; 200GB דיסק; Load Balancer של 10Mbps | **הבחירה.** האפשרות היחידה שבה גם ניהול האשכול וגם השרתים חינמיים לאורך זמן |
| GKE Autopilot | ניהול האשכול מכוסה בזיכוי של $74.40 לחודש; משאבי ההרצה בתשלום; $300 למשתמש חדש ל־90 יום | **חלופה מוכנה** ל־prod בבטא או אם אין מכסת A1 |
| LKE / DOKS / AKS Free | control plane חינם, שרתים בתשלום | יציב, אבל לא חינמי |
| Red Hat Developer Sandbox | חינם, מוגבל בזמן (כ־30 יום) | ללמידה בלבד, לא לסביבה קבועה |
| k3s על VPS (Hetzner) | זול, אבל מחירים עלו ב־2026 ושרתי ARM לא תמיד זמינים | הכי הרבה תחזוקה עצמית |

**הסיכון המרכזי:** חינם אצל Oracle הוא חכירה ולא הבטחה. ב־15 ביוני 2026 Oracle קיצצה בלי הודעה ציבורית את מכסת A1 מ־4 OCPU ו־24GB ל־2 OCPU ו־12GB, וזמינות A1 משתנה לפי אזור. לכן ההגנה היא ניידות: תשתית כקוד, Helm ו־Argo CD, ומעבר ל־GKE או LKE בתוך שעות.

מקורות: [InfoQ על קיצוץ המכסה](https://www.infoq.com/news/2026/07/oracle-cloud-free-tier-limits/), [Oracle Customer Connect](https://community.oracle.com/customerconnect/discussion/970310/oci-always-free-updated-ampere-a1-compute-allocation), [Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/resourceref.htm), [OKE pricing](https://www.oracle.com/cloud/cloud-native/kubernetes-engine/pricing), [GKE pricing](https://cloud.google.com/kubernetes-engine/pricing), [Google Cloud free trial](https://cloud.google.com/free), [Akamai LKE](https://www.akamai.com/products/kubernetes), [השוואת control plane](https://spendark.com/compare/doks-vs-eks-vs-aks-vs-gke/), [Red Hat Sandbox](https://developers.redhat.com/developer-sandbox/faq), [Hetzner 2026](https://privatedevops.com/news/hetzner-june-2026-cloud-price-increase-what-to-do), [Supabase pausing](https://supabase.com/kb/faqs/platform/free-project-pausing).

## איך מנהלים — `אושר`: GitOps; הכלים `מוצע`
| שכבה | כלי | הסבר |
| --- | --- | --- |
| תשתית כקוד | **OpenTofu** (קוד פתוח, תואם Terraform) + provider של OCI | הרשת והאשכול נוצרים מקוד; אפשר להקים מחדש או לעבור ספק |
| הגדרת האפליקציה | **Helm chart אחד** + `values-local.yaml`, `values-staging.yaml`, `values-prod.yaml` | כל ההבדלים בין הסביבות מפורשים ובמקום אחד |
| פריסה | **Argo CD** + ApplicationSet (אפליקציה לכל סביבה) | מה שרץ נגזר מ־Git; יש ממשק גרפי; נפוץ בשוק. Flux קל יותר, אבל בלי ממשק |
| קידום staging → prod | **PR** שמעדכן את ה־image tag ב־`values-prod.yaml` | פשוט וגלוי; rollback הוא revert. [Kargo](https://akuity.io/blog/kargo-gitops-promotion-layer) הוא שדרוג ללמידה אחרי הבטא |
| CI | GitHub Actions: בדיקות → image ל־amd64 ול־arm64 → GHCR → עדכון tag של staging | ARM נדרש בגלל A1 |
| סודות | Sealed Secrets | אין סודות גלויים ב־Git, ואין תלות בספק |
| כניסת תעבורה | Gateway API (Envoy Gateway או Traefik) + cert-manager | ingress-nginx כבר לא מקבל עדכונים מאז מרץ 2026. [InfoQ](https://www.infoq.com/news/2025/11/kubernetes-ingress-nginx) |
| ניטור | Sentry ו־PostHog כבר בתוכנית; Prometheus ו־Grafana בהמשך לצורכי למידה | — |

**מוצרי preview environments מנוהלים** (Okteto, Bunnyshell, Northflank) לא נדרשים: הם נועדו לסביבה לכל PR, ו־Argo CD מכסה את הצורך שלנו. Rancher הוא ממשק לניהול כמה אשכולות, ולא נחוץ כשיש אשכול אחד. [Qovery](https://www.qovery.com/blog/per-pull-request-ephemeral-kubernetes-environments-tools-compared), [Argo CD מול Flux](https://oneuptime.com/blog/post/2026-02-26-argocd-vs-fluxcd-2026/view)

## סדר הקמה
1. **local** (שלב 4 בתוכנית הבנייה): k3d, Helm ו־Argo CD מקומי. לומדים את כל הזרימה בלי ענן.
2. **staging** (שלב 3, ניסוי חמישי): OpenTofu מקים את OKE; Argo CD מסנכרן מאותו repo; בודקים חיבור JDBC ל־Supabase מתוך האשכול, כולל IPv4/IPv6 ו־SSL.
3. **production** (שלב 10, בטא): `values-prod.yaml`, Supabase Pro, התראת תקציב, והחלטה אם להפריד אשכול.

## עלות וזמן
- עד הבטא: $0, אם מכסת A1 זמינה. אם לא, GKE מכוסה מה־$300 בשלושת החודשים הראשונים.
- בבטא: כ־$25 לחודש ל־Supabase Pro, ודומיין.
- בכל ספק מגדירים התראת תקציב. התראה לא עוצרת חיוב אוטומטית.
- תוספת זמן ביחס ל־Cloud Run: כ־4–6 ימים, כולל OpenTofu. זו הערכה ולא מדידה.

## החלטות פתוחות
1. Helm או Kustomize. ההמלצה: Helm.
2. מתי מפרידים את production לאשכול נפרד, ואצל איזה ספק.
3. אזור ענן: לבדוק latency מישראל ולבחור אזור קרוב לאזור של Supabase. זמינות A1 משתנה לפי אזור.
4. חשבון Oracle: Always Free בלבד או Pay-As-You-Go. דווח שחשבונות PAYG שמרו על המכסה הישנה, אבל זה לא מאומת ויש סיכון לחיוב.
