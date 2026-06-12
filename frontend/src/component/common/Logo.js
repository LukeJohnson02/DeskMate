import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

/**
 * Shared DeskMate logo used in navigation and brand surfaces.
 *
 * The default parameter syntax keeps callers simple: most places can render
 * `<Logo />`, while tests or compact layouts can still override the icon size.
 */
const Logo = ({ size = "2x", className = "" }) => (
  <div className={`flex items-center gap-2 ${className}`}>
    <FontAwesomeIcon
      icon={["fab", "slideshare"]}
      size={size}
      className="text-blue-600"
    />
    <span className="text-xl font-bold text-gray-800">DeskMate</span>
  </div>
);

export default Logo;
