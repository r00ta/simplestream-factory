import { useEffect, useState } from "react";

// Modal Component for displaying the URL
interface ModalProps {
  isOpen: boolean;
  url: string;
  onClose: () => void;
}

const Modal = ({ isOpen, url, onClose }: ModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm mx-auto">
        <h3 className="text-xl font-semibold mb-4">Manifest URL</h3>
        <p className="text-gray-700 mb-4">Your manifest has been successfully generated. Add it to your MAAS and use the Ubuntu keyrings for verification.</p>
        <a
          href={url}
          className="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          {url}
        </a>
        <div className="mt-4 text-right">
          <button
            onClick={onClose}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default function ProductSelector() {
  const [products, setProducts] = useState<SimplestreamProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Record<number, number[]>>({});
  const [openProductIds, setOpenProductIds] = useState<Set<number>>(new Set());
  const [openOsGroups, setOpenOsGroups] = useState<Set<string>>(new Set());
  const [modalOpen, setModalOpen] = useState(false);
  const [simplestreamUrl, setSimplestreamUrl] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/v1/simplestreamproducts");
        const result: SimplestreamProductsResponse = await response.json();
        setProducts(result.items);
      } catch (err) {
        setError("Failed to fetch data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const toggleVersion = (productId: number, versionId: number) => {
    setSelected((prev) => {
      const current = prev[productId] || [];
      const updated = current.includes(versionId)
        ? current.filter((id) => id !== versionId)
        : [...current, versionId];
      return { ...prev, [productId]: updated };
    });
  };

  const toggleProductDropdown = (productId: number) => {
    setOpenProductIds((prev) => {
      const newSet = new Set(prev);
      newSet.has(productId) ? newSet.delete(productId) : newSet.add(productId);
      return newSet;
    });
  };

  const toggleOsGroup = (os: string) => {
    setOpenOsGroups((prev) => {
      const newSet = new Set(prev);
      newSet.has(os) ? newSet.delete(os) : newSet.add(os);
      return newSet;
    });
  };

  const handleSubmit = async () => {
    const versionIds = Object.values(selected).flat();

    if (versionIds.length === 0) {
      alert("Please select at least one version.");
      return;
    }

    try {
      const response = await fetch("/v1/simplestreamsmanifests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ version_ids: versionIds }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server responded with error: ${errorText}`);
      }

      const result = await response.json();
      console.log("Submission result:", result);

      // Open the modal and set the URL
      setSimplestreamUrl(result.simplestream_url);
      setModalOpen(true);
    } catch (err: any) {
      console.error("Submission failed:", err);
      alert(`Submission failed: ${err.message}`);
    }
  };

  const groupedByOs = products.reduce<Record<string, SimplestreamProduct[]>>((acc, product) => {
    if (!acc[product.os]) acc[product.os] = [];
    acc[product.os].push(product);
    return acc;
  }, {});

  if (loading) return <div className="p-4 text-gray-600">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <div className="max-w-5xl mx-auto bg-white rounded-xl shadow-xl p-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
          Product Version Selector
        </h1>

        <div className="space-y-6">
          {Object.entries(groupedByOs).map(([os, osProducts]) => (
            <div key={os} className="border rounded-lg bg-gray-50 shadow-sm">
              <button
                onClick={() => toggleOsGroup(os)}
                className="w-full text-left px-4 py-3 text-lg font-semibold bg-gray-100 hover:bg-gray-200 flex justify-between items-center"
              >
                <span>{os}</span>
                <span className="text-gray-500">{openOsGroups.has(os) ? "▲" : "▼"}</span>
              </button>

              {openOsGroups.has(os) && (
                <div className="px-4 pb-4 space-y-4">
                  {osProducts.map((product) => (
                    <div
                      key={product.id}
                      className="border border-gray-200 rounded-md bg-white shadow-sm"
                    >
                      <button
                        className="w-full text-left p-3 hover:bg-gray-50 flex justify-between items-center"
                        onClick={() => toggleProductDropdown(product.id)}
                      >
                        <div>
                          <div className="font-medium text-gray-800">{product.name}</div>
                          <div className="text-sm text-gray-500">Arch: {product.arch}</div>
                        </div>
                        <span className="text-gray-400 text-xl">
                          {openProductIds.has(product.id) ? "▲" : "▼"}
                        </span>
                      </button>

                      {openProductIds.has(product.id) && (
                        <div className="px-6 pb-4 transition-all duration-300">
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
                            {product.versions.map((version) => (
                              <label
                                key={version.id}
                                className="flex items-center gap-3 bg-gray-50 px-4 py-2 rounded-md border border-gray-200 hover:bg-blue-50 cursor-pointer"
                              >
                                <input
                                  type="checkbox"
                                  className="accent-blue-600 w-5 h-5"
                                  checked={selected[product.id]?.includes(version.id) || false}
                                  onChange={() => toggleVersion(product.id, version.id)}
                                />
                                <span className="text-sm text-gray-700">
                                  <span className="font-medium">{version.name}</span>{" "}
                                  <span className="text-xs text-gray-500">
                                    ({version.channel})
                                  </span>
                                </span>
                              </label>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-10 text-center">
          <button
            onClick={handleSubmit}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md"
          >
            Submit
          </button>
        </div>
      </div>

      {/* Modal for displaying URL */}
      <Modal
        isOpen={modalOpen}
        url={simplestreamUrl}
        onClose={() => setModalOpen(false)}
      />
    </div>
  );
}

// Types
interface SimplestreamProductVersion {
  id: number;
  name: string;
  channel: string;
}

interface SimplestreamProduct {
  id: number;
  name: string;
  arch: string;
  os: string;
  versions: SimplestreamProductVersion[];
}

interface SimplestreamProductsResponse {
  items: SimplestreamProduct[];
  total: number;
}
