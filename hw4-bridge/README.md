# HW4 bridge — automate your Part 3 Azure ship (optional bonus)

Today's lab taught you to wrap a service in a **CI/CD pipeline**. Here's how that connects
straight to **HW4**, honestly:

**What genuinely transfers from today → HW4**
- **Repo setup & submission.** "Use this template → keep it **Public**" is exactly how you
  create and submit your HW4 repo. You already did it.
- **The service.** HW4 deploys the same kind of fraud API (`/health` + `/predict`) you ran today.
- **The Azure target.** Today's pipeline ships to **Azure Container Apps** — that *is* HW4 **Part 3**.
- **The rollout idea.** The canary you saw is *why* HW4 asks for a rolling update + blue-green
  (**Part 2**): never drop a request.

**What today did NOT do (so you know)**
- It is **not** the HW4 **Kubernetes** work — **Part 1** (3 replicas, probes, HPA, self-healing) is
  `kubectl` in your kit, with Minikube/Codespaces. Do that part in the kit.
- The **CI/CD pipeline + eval gate** is a **professional practice you can add for the +10 bonus** —
  it is **not required** to pass HW4. But it's real, and it makes a deploy safe.

## The optional bonus: make your HW4 repo deploy itself

`ship-to-azure.yml` is a GitHub Actions workflow that runs your kit's **provided** `deploy_azure.sh`
automatically, instead of by hand in Cloud Shell.

1. Copy `ship-to-azure.yml` into your **HW4 repo** at `.github/workflows/ship-to-azure.yml`.
2. One-time OIDC setup: create an Azure AD app + **federated credential** and add three repo secrets —
   `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`. (OIDC = no keys.)
3. **Actions** tab → **hw4-ship-to-azure** → **Run workflow**. It imports the image, deploys to
   Container Apps, and prints your public `/predict` URL.
4. **Cost rule (same as HW4):** capture your evidence, then **tear it down the same day**.

> The **required** HW4 Part 3 path is still `deploy_azure.sh` in **Azure Cloud Shell**
> (see `AZURE-QUICKSTART.md` in your kit). This workflow is a bonus on top of that.
