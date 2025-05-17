// src/components/Offcanvas.jsx
import { XMarkIcon }  from "@heroicons/react/24/solid";
import { createPortal } from "react-dom";

export default function Offcanvas({ open, onClose, children }) {
  if (!open) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex">
      {/* backdrop */}
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      {/* panel */}
      <aside className="relative ml-auto h-full w-80 max-w-[90%] bg-white p-6 overflow-y-auto shadow-xl">
        <button onClick={onClose} className="mb-4 text-gray-500 hover:text-gray-700">
          <XMarkIcon className="w-6 h-6" />
        </button>
        {children}
      </aside>
    </div>,
    document.body
  );
}
