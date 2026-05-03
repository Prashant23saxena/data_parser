import { expect, test } from "@playwright/test";

const connectionPayload = {
  connectionName: "Client Odoo",
  odooUrl: "client.odoo.com",
  dbName: "client-db",
  username: "admin",
  apiKey: "secret-key"
};

test("configures Odoo, browses fields, and fetches records into catalog", async ({ page }) => {
  await page.route("**/api/storage/status", async (route) => {
    await route.fulfill({
      json: {
        status: "ready",
        databaseReady: true,
        databasePath: "/tmp/kriyax.duckdb",
        workspaceRoot: "/tmp/kriyax",
        checkedAt: "2026-05-02T00:00:00Z",
        error: null
      }
    });
  });
  await page.route("**/api/odoo/test-connection", async (route) => {
    expect(await route.request().postDataJSON()).toMatchObject(connectionPayload);
    await route.fulfill({
      json: {
        status: "success",
        message: "Connected successfully to https://client.odoo.com (Odoo 17.0).",
        odooUrl: "https://client.odoo.com",
        version: "17.0",
        uid: 7
      }
    });
  });
  await page.route("**/api/odoo/connections", async (route) => {
    await route.fulfill({ json: { ...connectionPayload, apiKey: "********" } });
  });
  await page.route("**/api/odoo/models**", async (route) => {
    const requestUrl = new URL(route.request().url());
    if (requestUrl.pathname.endsWith("/fields")) {
      await route.fulfill({
        json: {
          fields: [
            { name: "id", label: "ID", type: "integer", required: false, readonly: true, relation: null, supported: true },
            { name: "name", label: "Name", type: "char", required: true, readonly: false, relation: null, supported: true },
            { name: "company_id", label: "Company", type: "many2one", required: false, readonly: false, relation: "res.company", supported: true },
            { name: "image_1920", label: "Image", type: "binary", required: false, readonly: true, relation: null, supported: false, warning: "Binary fields excluded from import" }
          ]
        }
      });
      return;
    }
    await route.fulfill({
      json: {
        models: [
          { model: "res.partner", name: "Contacts", fieldCount: 4 },
          { model: "sale.order", name: "Sales Order", fieldCount: 2 }
        ]
      }
    });
  });
  await page.route("**/api/odoo/fetch", async (route) => {
    expect(await route.request().postDataJSON()).toMatchObject({
      modelName: "res.partner",
      targetSchema: "raw_odoo",
      tableName: "res_partner"
    });
    await route.fulfill({
      json: {
        qualifiedName: "raw_odoo.res_partner",
        schema: "raw_odoo",
        tableName: "res_partner",
        rowCount: 2,
        columnCount: 4,
        createdAt: "2026-05-02T00:00:00Z",
        source: { kind: "odoo", connectionName: "Client Odoo", model: "res.partner" },
        columns: [],
        warnings: ["Binary fields excluded from import: image_1920"]
      }
    });
  });

  await page.goto("/connectors/odoo");
  await page.getByLabel("Connection name").fill(connectionPayload.connectionName);
  await page.getByLabel("Odoo URL").fill(connectionPayload.odooUrl);
  await page.getByLabel("Database").fill(connectionPayload.dbName);
  await page.getByLabel("Username").fill(connectionPayload.username);
  await page.getByLabel("API key").fill(connectionPayload.apiKey);

  await page.getByRole("button", { name: "Test connection" }).click();
  await expect(page.getByText("Connected successfully to https://client.odoo.com (Odoo 17.0).")).toBeVisible();
  await expect(page.getByText("Connection 'Client Odoo' saved.")).toBeVisible();
  await expect(page.getByRole("cell", { name: "res.partner", exact: true })).toBeVisible();

  await page.getByLabel("Search models").fill("sale");
  await page.getByRole("button", { name: "Load models" }).click();
  await expect(page.getByRole("cell", { name: "sale.order", exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Open res.partner" }).click();
  await expect(page.getByText("company_id")).toBeVisible();
  await expect(page.getByText("Company · many2one -> res.company")).toBeVisible();
  await expect(page.getByText("image_1920")).toBeVisible();
  await expect(page.getByText("Binary fields excluded from import")).toBeVisible();

  await page.getByLabel("New table name").fill("res_partner");
  await page.getByRole("button", { name: "Fetch records" }).click();
  await expect(page.getByText("Table 'raw_odoo.res_partner' created with 2 rows.")).toBeVisible();
});
