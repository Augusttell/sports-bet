import os

import lightgbm as lgbm
from sklearn.decomposition import PCA
# TODO IMPORT UMAP
##
# Use both as data
from sklearn.model_selection import train_test_split



training_data = read_csv(os.getcwd() + "/data/training_data.csv")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,
                                                    random_state=42)


# Perform PCA
pca_threshold = 0.95

pca = PCA()
pca.fit(X_train)

reduced_train = PCA(n_components=pca_threshold).fit_transform(X_train)


reduced_train


# Performs kmeans and PCA
def pca_kmeans(df,
               variables_used,
               path,
               prefix,
               pca_threshold=0.95,
               max_clusters=50):
    # Dimension reduction
    pca = PCA()
    pca.fit(df[variables_used])

    # Compute components
    reduced_data = PCA(n_components=pca_threshold).fit_transform(
        df[variables_used])

    # Internal scores of clustering
    Sum_of_squared_distances = []
    silhouette_score = []
    davies_bouldin_score = []
    calinski_harabasz_score = []

    K = range(2, max_clusters)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(reduced_data)
        Sum_of_squared_distances.append(km.inertia_)
        silhouette_score.append(
            metrics.silhouette_score(X=reduced_data,
                                     labels=km.labels_,
                                     metric='euclidean'))
        davies_bouldin_score.append(
            metrics.davies_bouldin_score(X=reduced_data, labels=km.labels_))

    plt.figure(0)
    plt.plot(K, silhouette_score, 'bx-')
    plt.xlabel('k')
    plt.ylabel('silhouette_score')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "silhouette_score.png")

    plt.figure(1)
    plt.plot(range(3, max_clusters), np.diff(silhouette_score), 'bx-')
    plt.xlabel('k')
    plt.ylabel('silhouette_score_diff')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "silhouette_score_diff.png")

    plt.figure(2)
    plt.plot(K, davies_bouldin_score, 'bx-')
    plt.xlabel('k')
    plt.ylabel('davies_bouldin_score')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "davies_bouldin_score.png")

    plt.figure(3)
    plt.plot(range(3, max_clusters), np.diff(davies_bouldin_score), 'bx-')
    plt.xlabel('k')
    plt.ylabel('davies_bouldin_score_diff')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "davies_bouldin_score_diff.png")

    plt.figure(4)
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "sum_of_squared_distances.png")

    plt.figure(5)
    plt.plot(range(3, max_clusters), np.diff(Sum_of_squared_distances), 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances_diff')
    plt.title('Elbow Method For Optimal k')
    plt.savefig(path + prefix + "sum_of_squared_distances_diff.png")

    results = pd.DataFrame(
        {
            "silhouette_score": silhouette_score,
            "davies_bouldin_score": davies_bouldin_score,
            "Sum_of_squared_distances": Sum_of_squared_distances
        },
        index=K)
    return results


# Set parameters used for dimension reduction
n_neighbors_articles = 5 * 2
local_connectivity_articles = 5
min_dist_articles = np.round(
    np.abs(bert_embeddings[
               [s for s in bert_embeddings.columns if "embedding" in s]].median(
        axis=1).median() -
           bert_embeddings[
               [s
                for s in bert_embeddings.columns if "embedding" in s]].mean(
               axis=1).median()),
    5)

# Run dimension reduction
reducer = umap.UMAP(n_neighbors=n_neighbors_articles,
                    local_connectivity=local_connectivity_articles,
                    min_dist=min_dist_articles,
                    n_components=10,
                    random_state=42,
                    n_epochs=500,
                    metric="cosine")

UMAP = reducer.fit_transform(
    bert_embeddings[[s for s in bert_embeddings.columns if "embedding" in s]])

# Add embeddings to variables
bert_embeddings['umap_projection_0'] = UMAP[:, 0]
bert_embeddings['umap_projection_1'] = UMAP[:, 1]
bert_embeddings['umap_projection_2'] = UMAP[:, 2]
bert_embeddings['umap_projection_3'] = UMAP[:, 3]
bert_embeddings['umap_projection_4'] = UMAP[:, 4]
bert_embeddings['umap_projection_5'] = UMAP[:, 5]
bert_embeddings['umap_projection_6'] = UMAP[:, 6]
bert_embeddings['umap_projection_7'] = UMAP[:, 7]
bert_embeddings['umap_projection_8'] = UMAP[:, 8]
bert_embeddings['umap_projection_9'] = UMAP[:, 9]

# Write data
bert_embeddings.to_csv(path + "umapped_embeddings.csv", index=None)