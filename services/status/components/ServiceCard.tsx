export default function ServiceCard({name, status}: { name: string; status: string }) {
    return (
        <div className={`p-4 border rounded-lg shadow-lg ${status === "UP" ? "bg-green-200" : "bg-red-200"}`}>
            <h2 className="text-xl font-semibold">{name}</h2>
            <p className={`mt-2 font-bold ${status === "UP" ? "text-green-700" : "text-red-700"}`}>{status}</p>
        </div>
    );
}
