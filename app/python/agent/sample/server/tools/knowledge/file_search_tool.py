import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, VectorStore, VectorStoreDataSource, VectorStoreDataSourceAssetType


def create_file_search_tool(project_client: AIProjectClient) -> FileSearchTool:
    current_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(current_dir, "assets")
    
    asset_uris = []
    for filename in os.listdir(assets_dir):
        full_path = os.path.join(assets_dir, filename)
        if os.path.isfile(full_path):
            _, asset_uri = project_client.upload_file(full_path)
            print(f"Uploaded file, asset URI: {asset_uri}")
            asset_uris.append(asset_uri)
    
    data_sources = [VectorStoreDataSource(asset_identifier=uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET) for uri in asset_uris]
    vector_store: VectorStore = project_client.agents.create_vector_store_and_poll(data_sources=data_sources, name="sample_vector_store")
    print(f"Created vector store, vector store ID: {vector_store.id}")

    return FileSearchTool(vector_store_ids=[vector_store.id])