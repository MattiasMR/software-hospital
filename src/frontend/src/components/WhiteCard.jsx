export default function WhiteCard({ children, className = "" }) {
  return (
    <div className={`bg-white bg-opacity-80 backdrop-blur-md rounded-2xl shadow-2xl ${className}`}>
      {children}
    </div>
  );
}
