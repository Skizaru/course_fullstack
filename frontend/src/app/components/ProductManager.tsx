'use client'
import { useState, useEffect } from 'react';
const backendUri = process.env.NEXT_PUBLIC_BACKEND_URL;
const productUri = `${backendUri}/api/product`

interface Product {
  id: number;
  name: string;
  comment: string;
  quantity: number;
  company_id: string;
  company?: any; // TODO : Define the company manager and model
}

export default function ProductManager() {
  const [products, setProducts] = useState<Product[]>([]);
  const [newProduct, setNewProduct] = useState<Partial<Product>>({
    name: '',
    comment: '',
    quantity: 0,
    company_id: ''
  });
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  // Fetch products on initial load
  useEffect(() => {
    fetch(productUri)
      .then((res) => res.json())
      .then((data) => setProducts(data.data));
  }, []);

  // Add a new product
  const addProduct = async () => {
    if (!newProduct.name || !newProduct.comment || newProduct.quantity === undefined || !newProduct.company_id) {
      alert('Please fill in all fields.');
      return;
    }

    const res = await fetch(productUri, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newProduct),
    });
    const product = await res.json();
    setProducts((prev) => [...prev, product]);
    setNewProduct({ name: '', comment: '', quantity: 0, company_id: '' });
  };

  // Update an existing product
  const updateProduct = async () => {
    if (!editingProduct) return;

    const res = await fetch(`${productUri}/${editingProduct.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingProduct),
    });
    await res.json();
    setProducts((prev) =>
      prev.map((p) => (p.id === editingProduct.id ? editingProduct : p))
    );
    setEditingProduct(null);
  };

  // Delete a product
  const deleteProduct = async (id: number) => {
    await fetch(`${productUri}/${id}`, { method: 'DELETE' });
    setProducts((prev) => prev.filter((p) => p.id !== id));
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Product Manager</h1>

      {/* Add a New Product */}
      <div className="mb-4">
        <input
          type="text"
          className="border p-2 mr-2"
          placeholder="Product name"
          value={newProduct.name}
          onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
        />
        <input
          type="text"
          className="border p-2 mr-2"
          placeholder="Comment"
          value={newProduct.comment}
          onChange={(e) => setNewProduct({ ...newProduct, comment: e.target.value })}
        />
        <input
          type="number"
          className="border p-2 mr-2"
          placeholder="Quantity"
          value={newProduct.quantity}
          onChange={(e) =>
            setNewProduct({ ...newProduct, quantity: parseInt(e.target.value, 10) })
          }
        />

<input
          type="text"
          className="border p-2 mr-2"
          placeholder="Company id"
          value={newProduct.company_id}
          onChange={(e) =>
            setNewProduct({ ...newProduct, company_id: e.target.value })
          }
        />
        <button
          onClick={addProduct}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Product
        </button>
      </div>

      {/* List of Products */}
      <ul>
        {products.map((product) => (
          <li key={product.id} className="mb-2 flex items-center">
            <div className="flex-1">
              <span className="font-bold">{product.name}</span> - {product.comment} (
              {product.quantity}) from {product.company.name} ({product.company_id})
            </div>
            <button
              onClick={() => setEditingProduct(product)}
              className="bg-yellow-500 text-white px-2 py-1 rounded mr-2"
            >
              Edit
            </button>
            <button
              onClick={() => deleteProduct(product.id)}
              className="bg-red-500 text-white px-2 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {/* Edit Product */}
      {editingProduct && (
        <div className="mt-4">
          <input
            type="text"
            className="border p-2 mr-2"
            placeholder="Product name"
            value={editingProduct.name}
            onChange={(e) =>
              setEditingProduct({ ...editingProduct, name: e.target.value })
            }
          />
          <input
            type="text"
            className="border p-2 mr-2"
            placeholder="Comment"
            value={editingProduct.comment}
            onChange={(e) =>
              setEditingProduct({ ...editingProduct, comment: e.target.value })
            }
          />
          <input
            type="number"
            className="border p-2 mr-2"
            placeholder="Quantity"
            value={editingProduct.quantity}
            onChange={(e) =>
              setEditingProduct({
                ...editingProduct,
                quantity: parseInt(e.target.value, 10),
              })
            }
          />
<input
            type="text"
            className="border p-2 mr-2"
            placeholder="Company id"
            value={editingProduct.company_id}
            onChange={(e) =>
              setEditingProduct({ ...editingProduct, company_id: e.target.value })
            }
          />
          <button
            onClick={updateProduct}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Update Product
          </button>
        </div>
      )}
    </div>
  );
}
