using '../templates/container.bicep'

param acrName = 'acrmcwfy25q2g9112'  // ChangeMe（末尾の数字を変える）

param workspaceName = 'log-mcw25q2g9112'  // ChangeMe（末尾の数字を変える）
param appInsightsName = 'appi-mcwfy25q2g9112'  // ChangeMe（末尾の数字を変える）

param environmentName = 'managedEnvironment-mcwfy25q2g9112'  // ChangeMe（末尾の数字を変える）

// Spoke VNET の名前
param vnetName = 'vnet-mcwfy25q2g9112-spoke'  // ChangeMe（スポークVNETの名前を指定）
param subnetName = 'ContainerAppsSubnet'

param containerAppsName = 'ca-mcwfy25q2g9112'  // ChangeMe（末尾の数字を変える）

param location = 'westus'
