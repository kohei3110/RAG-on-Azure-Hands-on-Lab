using '../templates/bastion.bicep'

// Bastion を展開する仮想ネットワーク (Hub)
param vnetName = 'vnet-hub-mcwfy25q2g9112-hub'  // ChangeMe（ハブVNETの名前を指定）
param addressPrefix = '10.0.0.0/16'

// サブネット
param subnetPrefix = '10.0.10.0/26'

// リソースを展開する際に使用するネットワークの名前（Spoke）
param spokeNetworkName = 'vnet-mcwfy25q2g9112-spoke'  // ChangeMe（スポークVNETの名前を指定）

// Bastion Host の名前
param bastionName = 'bas-mcwfy25q2g9112'  // ChangeMe（末尾の数字を変える）

param location = 'westus'
