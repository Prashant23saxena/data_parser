import { expect, test } from "@playwright/test";

test("creates a pipeline from a saved script and runs it manually", async ({ page }) => {
  const suffix = Date.now();
  const scriptName = `pipeline_hello_${suffix}.py`;
  const pipelineName = `Pipeline ${suffix}`;

  await page.goto("/code");
  await page.getByLabel("Script name").fill(scriptName);
  await page.locator("textarea").fill(`print("pipeline hello ${suffix}")\n`);
  await page.getByRole("button", { name: "Run script" }).click();
  await expect(page.getByText("Success")).toBeVisible();
  await expect(page.getByText(`pipeline hello ${suffix}`, { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Pipelines" }).click();
  await page.getByLabel("Pipeline name").fill(pipelineName);
  await page.getByLabel("Saved script").selectOption(scriptName);
  await page.getByRole("button", { name: "Create pipeline" }).click();

  await expect(page.getByText(`Pipeline '${pipelineName}' saved.`)).toBeVisible();
  await expect(page.getByRole("cell", { name: pipelineName })).toBeVisible();
  await expect(page.getByRole("cell", { name: scriptName })).toBeVisible();
  const pipelineRow = page.getByRole("row").filter({ hasText: pipelineName });

  await pipelineRow.getByLabel(`Schedule type for ${pipelineName}`).selectOption("daily");
  await pipelineRow.getByLabel(`Time of day for ${pipelineName}`).fill("06:00");
  await pipelineRow.getByLabel(`Timezone for ${pipelineName}`).fill("Asia/Kolkata");
  await pipelineRow.getByRole("button", { name: "Save schedule" }).click();
  await expect(page.getByText(new RegExp(`${pipelineName} schedule saved\\. Next run`))).toBeVisible();
  await expect(pipelineRow.getByText(/daily · next/)).toBeVisible();

  await pipelineRow.getByRole("button", { name: "Disable" }).click();
  await expect(page.getByText(`${pipelineName} is now disabled.`)).toBeVisible();
  await expect(pipelineRow.locator(".status-text", { hasText: "disabled" })).toBeVisible();

  await pipelineRow.getByRole("button", { name: "Run now" }).click();
  await expect(page.locator("h1", { hasText: "Pipeline Run Detail" })).toBeVisible();
  await expect(page.getByText(pipelineName)).toBeVisible();
  await expect(page.getByText(scriptName)).toBeVisible();
  await expect(page.locator("pre").filter({ hasText: `pipeline hello ${suffix}` })).toBeVisible();
});
